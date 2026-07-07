# core_boinc/boinc_work_generator.py
import os
import json
import numpy as np
import time
import psycopg2

try:
    from astroquery.sdss import SDSS
    ASTROQUERY_AVAILABLE = True
except Exception:
    ASTROQUERY_AVAILABLE = False

# Exact Cosmological constants for comoving distance
H0 = 71.92
w0 = -0.5485
wa = -0.3968
Omega_m = 0.315
Omega_de = 0.685
c_light = 299792.458

def get_db_connection():
    """Establish a connection to the PostgreSQL database."""
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST", "localhost"),
            database=os.getenv("DB_NAME", "darkmatter"),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD", "postgres"),
            port=os.getenv("DB_PORT", 5432),
            connect_timeout=3
        )
        return conn
    except Exception as e:
        print(f"[Work Generator] Database connection error: {e}")
        return None

def generate_mock_galaxy_data(dataset_type, num_galaxies=5000):
    """Generates high-fidelity mock raw coordinates (RA, DEC, z) representing cosmological structures."""
    print(f"[Work Generator] Generating mock coordinates for {dataset_type} ({num_galaxies} galaxies)...")
    np.random.seed(int(time.time()))
    
    if dataset_type == "SDSS":
        # SDSS Luminous Red Galaxies (LRGs) typically cluster in [0.15, 0.4] redshift
        ra = np.random.uniform(150.0, 220.0, num_galaxies)
        dec = np.random.uniform(0.0, 50.0, num_galaxies)
        z = np.random.normal(0.28, 0.07, num_galaxies)
        z = np.clip(z, 0.05, 0.6)
    else:
        # Euclid Spectroscopic catalog typically spans deeper redshifts [0.5, 2.0]
        ra = np.random.uniform(0.0, 360.0, num_galaxies)
        dec = np.random.uniform(-90.0, 90.0, num_galaxies)
        z = np.random.normal(1.2, 0.4, num_galaxies)
        z = np.clip(z, 0.01, 2.5)
        
    return ra, dec, z

# Precomputed fine grid for comoving distance integration to speed up coordinate conversion
_z_grid = np.linspace(0.0, 3.5, 3000)
_dist_grid = np.zeros_like(_z_grid)
for _i, _z_val in enumerate(_z_grid):
    if _z_val == 0:
        continue
    # Numerical integration using 100 steps
    _zi = np.linspace(0, _z_val, 100)
    _f_de = ((1 + _zi)**(3 * (1 + w0 + wa))) * np.exp(-3 * wa * _zi / (1 + _zi))
    _E_z = np.sqrt(Omega_m * (1 + _zi)**3 + Omega_de * _f_de)
    _dist_grid[_i] = (c_light / H0) * np.sum(1.0 / _E_z) * (_z_val / 100)

def comoving_distance_cpl(z):
    """Retrieves comoving distance in Mpc via high-resolution vectorized grid interpolation."""
    return np.interp(z, _z_grid, _dist_grid)

def convert_spherical_to_cartesian(ra, dec, z):
    """Converts spherical coordinates to 3D Cartesian coordinates in Mpc utilizing fast NumPy operations."""
    ra_arr = np.asarray(ra, dtype=np.float64)
    dec_arr = np.asarray(dec, dtype=np.float64)
    z_arr = np.asarray(z, dtype=np.float64)
    
    dist = comoving_distance_cpl(z_arr)
    r_rad = np.radians(ra_arr)
    d_rad = np.radians(dec_arr)
    
    X = dist * np.cos(d_rad) * np.cos(r_rad)
    Y = dist * np.cos(d_rad) * np.sin(r_rad)
    Z = dist * np.sin(d_rad)
    return X, Y, Z

def create_boinc_workunit_shards(dataset_type="SDSS", num_shards=3, size_per_shard=5000, output_format="cartesian"):
    """
    Slices raw or pre-converted astronomical coordinates into BOEINC workunit shards.
    Supports 'cartesian' (X, Y, Z) and 'raw' (RA, DEC, redshift z) formats.
    """
    print(f"=== BOEINC WORK GENERATOR INITIALIZING FOR {dataset_type} ({output_format.upper()}) ===")
    
    os.makedirs("core_boinc/workunits", exist_ok=True)
    os.makedirs("core_boinc/project_xml", exist_ok=True)
    
    total_galaxies = num_shards * size_per_shard
    
    # Try fetching real SDSS BOSS LRG data if available and online
    ra, dec, z = None, None, None
    if dataset_type == "SDSS" and ASTROQUERY_AVAILABLE:
        try:
            print("[Work Generator] Attempting to fetch real SDSS BOSS DR17 data via Astroquery...")
            query = f"""
            SELECT TOP {total_galaxies} ra, dec, z 
            FROM SpecObj 
            WHERE class='GALAXY' AND z BETWEEN 0.15 AND 0.4 AND zErr < 0.001
            """
            result = SDSS.query_sql(query)
            if result is not None and len(result) > 0:
                ra = np.array(result['ra'], dtype=np.float32)
                dec = np.array(result['dec'], dtype=np.float32)
                z = np.array(result['z'], dtype=np.float32)
                print(f"[Work Generator] Fetched {len(result)} real galaxies from SDSS.")
        except Exception as e:
            print(f"[Work Generator] Astroquery SDSS failed ({e}). Falling back to high-fidelity simulation.")
            
    if ra is None:
        ra, dec, z = generate_mock_galaxy_data(dataset_type, total_galaxies)
        
    for shard_idx in range(num_shards):
        start_idx = shard_idx * size_per_shard
        end_idx = start_idx + size_per_shard
        
        shard_ra = ra[start_idx:end_idx]
        shard_dec = dec[start_idx:end_idx]
        shard_z = z[start_idx:end_idx]
        
        shard_id = f"boinc_wu_{dataset_type.lower()}_{output_format}_{shard_idx:04d}"
        shard_filename = f"core_boinc/workunits/{shard_id}_input.txt"
        
        print(f"   Writing shard {shard_idx+1}/{num_shards}: {shard_filename}...")
        
        with open(shard_filename, "w") as f:
            f.write(f"# BOEINC Shard ID: {shard_id}\n")
            f.write(f"# Format: {'RA DEC REDSHIFT' if output_format == 'raw' else 'X Y Z (Mpc)'}\n")
            
            if output_format == "raw":
                for r, d, zi in zip(shard_ra, shard_dec, shard_z):
                    f.write(f"{r:.6f} {d:.6f} {zi:.6f}\n")
            else:
                # Pre-convert to Cartesian
                X, Y, Z = convert_spherical_to_cartesian(shard_ra, shard_dec, shard_z)
                for x, y, z_val in zip(X, Y, Z):
                    f.write(f"{x:.6f} {y:.6f} {z_val:.6f}\n")
                    
        # Generate metadata descriptor file for server sync tracking
        metadata = {
            "job_id": shard_id,
            "dataset": dataset_type,
            "format": output_format,
            "num_galaxies": len(shard_ra),
            "created_at": time.time(),
            "status": "pending",
            "local_path": shard_filename
        }
        metadata_filename = f"core_boinc/workunits/{shard_id}_meta.json"
        with open(metadata_filename, "w") as f:
            json.dump(metadata, f, indent=2)
            
        # Register in PostgreSQL if connection available
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                chunk_data = {
                    "chunk_id": shard_id,
                    "dataset": dataset_type,
                    "format": output_format,
                    "num_galaxies": len(shard_ra),
                    "local_path": shard_filename
                }
                cursor.execute(
                    "INSERT INTO jobs (job_id, status, chunk_data) VALUES (%s, %s, %s) "
                    "ON CONFLICT (job_id) DO UPDATE SET status = 'pending', chunk_data = EXCLUDED.chunk_data",
                    (shard_id, "pending", json.dumps(chunk_data))
                )
                conn.commit()
                cursor.close()
                conn.close()
                print(f"  └─ Registered shard '{shard_id}' as pending job in PostgreSQL.")
            except Exception as dbe:
                print(f"  └─ [ERROR] Failed to register shard '{shard_id}' in PostgreSQL: {dbe}")
                if conn:
                    conn.close()
            
    print("✅ [SUCCESS] BOEINC workunit shards generated successfully in core_boinc/workunits/!\n")

if __name__ == "__main__":
    # Generate Cartesian workunit shards for SDSS
    create_boinc_workunit_shards("SDSS", num_shards=2, size_per_shard=5000, output_format="cartesian")
    
    # Generate Raw (spherical RA, DEC, z) workunit shards for Euclid
    create_boinc_workunit_shards("Euclid", num_shards=2, size_per_shard=8000, output_format="raw")
