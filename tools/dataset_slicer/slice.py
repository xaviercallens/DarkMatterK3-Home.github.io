# tools/dataset_slicer/slice.py
import os
import json
import numpy as np

# Cosmological constants matching our pipeline
H0 = 71.92
w0 = -0.5485
wa = -0.3968
Omega_m = 0.315
Omega_de = 0.685
c_light = 299792.458

def comoving_distance(z):
    """Calcule la distance comobile en Mpc."""
    steps = 50
    z_vals = np.linspace(0, z, steps)
    dz = z / steps if z > 0 else 0
    integrand = 0
    for zi in z_vals:
        f_de = ((1 + zi)**(3 * (1 + w0 + wa))) * np.exp(-3 * wa * zi / (1 + zi))
        E_z = np.sqrt(Omega_m * (1 + zi)**3 + Omega_de * f_de)
        integrand += 1.0 / E_z
    return (c_light / H0) * integrand * dz

def slice_and_package_dataset(output_dir, num_sectors=35):
    """Generates pre-sliced 500KB chunks of galaxies for high-speed client WASM download."""
    os.makedirs(output_dir, exist_ok=True)
    print(f"Starting dataset slicing for {num_sectors} cosmic sectors...")

    # Generate coordinate sectors resembling SDSS BOSS DR17 footprint
    # RA: 150-220, DEC: 0-50
    ra_steps = np.linspace(150.0, 220.0, 8)
    dec_steps = np.linspace(0.0, 50.0, 6)
    
    sectors = []
    for i in range(len(ra_steps) - 1):
        for j in range(len(dec_steps) - 1):
            sectors.append({
                "ra_min": float(ra_steps[i]),
                "ra_max": float(ra_steps[i+1]),
                "dec_min": float(dec_steps[j]),
                "dec_max": float(dec_steps[j+1])
            })

    for idx, sector in enumerate(sectors[:num_sectors]):
        np.random.seed(idx + 1000)
        num_galaxies = np.random.randint(4000, 7500)
        
        # Simulate galaxies
        ra = np.random.uniform(sector["ra_min"], sector["ra_max"], num_galaxies)
        dec = np.random.uniform(sector["dec_min"], sector["dec_max"], num_galaxies)
        z = np.random.normal(0.28, 0.07, num_galaxies)
        z = np.clip(z, 0.05, 0.6)
        
        # Convert to 3D Cartesian coordinates
        X, Y, Z = [], [], []
        for r, d, zi in zip(ra, dec, z):
            dist = comoving_distance(zi)
            r_rad = np.radians(r)
            d_rad = np.radians(d)
            X.append(float(dist * np.cos(d_rad) * np.cos(r_rad)))
            Y.append(float(dist * np.cos(d_rad) * np.sin(r_rad)))
            Z.append(float(dist * np.sin(d_rad)))
            
        # Compile payload
        payload = {
            "sector_index": idx,
            "ra_range": [sector["ra_min"], sector["ra_max"]],
            "dec_range": [sector["dec_min"], sector["dec_max"]],
            "num_galaxies": num_galaxies,
            "coordinates": {
                "x": X,
                "y": Y,
                "z": Z
            }
        }
        
        # Write to JSON chunk file (target size ~500KB)
        file_path = os.path.join(output_dir, f"shard_{idx:04d}.json")
        with open(file_path, "w") as f:
            json.dump(payload, f)
            
        # Verify size
        size_kb = os.path.getsize(file_path) / 1024.0
        print(f"  └─ Shard {idx:04d} created successfully: {size_kb:.2f} KB | {num_galaxies} galaxies")

    # Save manifest index
    manifest = {
        "num_shards": len(sectors),
        "cosmology": {
            "h0": H0,
            "w0": w0,
            "wa": wa,
            "omega_m": Omega_m,
            "omega_de": Omega_de
        },
        "shards": [f"shard_{i:04d}.json" for i in range(len(sectors))]
    }
    with open(os.path.join(output_dir, "manifest.json"), "w") as f:
        json.dump(manifest, f, indent=2)
    print("Dataset slicing and packaging complete! Manifest saved.")

if __name__ == "__main__":
    import sys
    target_dir = sys.argv[1] if len(sys.argv) > 1 else "../../ui_loom/public/data"
    slice_and_package_dataset(target_dir)
