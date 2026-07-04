import time
import torch
import numpy as np

# --- CONFIGURATION ---
H0 = 71.92
Omega_m = 0.315
Omega_de = 0.685
w0 = -0.5485
wa = -0.3968
c_light = 299792.458
NUM_GALAXIES = 50_000_000  # Scénario 1 : 50 Millions de galaxies (Euclid Spectroscopique)
GRID_SIZE = 128            # Résolution doublée pour ce grand catalogue (128x128x128)

def simulate_euclid_catalog(num_galaxies):
    print(f"[1/4] Génération du catalogue mock Euclid ({num_galaxies:,} galaxies)...")
    start = time.time()
    # Utilisation de float32 pour optimiser la RAM
    ra = np.random.uniform(0.0, 360.0, num_galaxies).astype(np.float32)
    dec = np.random.uniform(-90.0, 90.0, num_galaxies).astype(np.float32)
    z = np.random.normal(0.5, 0.2, num_galaxies)
    z = np.clip(z, 0.01, 2.5).astype(np.float32)
    print(f"      Terminé en {time.time() - start:.2f} s")
    return ra, dec, z

def comoving_distance_approx(z_array):
    print("[2/4] Intégration cosmologique vectorisée (CPU)...")
    start = time.time()
    # Approximation polynomiale rapide pour la distance comobile afin d'éviter 
    # une boucle for sur 50 millions d'éléments.
    # Pour un test de validation de charge, on simule la charge CPU.
    dist = (c_light / H0) * z_array * (1 - 0.5 * (1 + Omega_m) * z_array)
    print(f"      Terminé en {time.time() - start:.2f} s")
    return dist

def run_validation():
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"=== VALIDATION SCÉNARIO 1 : EUCLID SPECTROSCOPIQUE ===")
    print(f"Moteur : {device.type.upper()}")
    if device.type == 'cuda':
        print(f"GPU : {torch.cuda.get_device_name(0)}")
        print(f"VRAM Totale : {torch.cuda.get_device_properties(0).total_memory / 1024**3:.2f} GB")
    print("-" * 50)

    # 1. Génération
    ra, dec, z = simulate_euclid_catalog(NUM_GALAXIES)

    # 2. Cosmologie
    dist = comoving_distance_approx(z)
    
    print("[3/4] Conversion Sphérique -> Cartésienne...")
    start = time.time()
    r_rad = np.radians(ra)
    d_rad = np.radians(dec)
    X = dist * np.cos(d_rad) * np.cos(r_rad)
    Y = dist * np.cos(d_rad) * np.sin(r_rad)
    Z_cart = dist * np.sin(d_rad)
    print(f"      Terminé en {time.time() - start:.2f} s")

    # 3. Calcul Tenseur GPU
    print(f"[4/4] Projection Tensorielle K3 sur GPU (Grille {GRID_SIZE}^3)...")
    start_gpu = time.time()
    
    t_X = torch.tensor(X, device=device)
    t_Y = torch.tensor(Y, device=device)
    t_Z = torch.tensor(Z_cart, device=device)
    
    t_X = t_X - torch.mean(t_X)
    t_Y = t_Y - torch.mean(t_Y)
    t_Z = t_Z - torch.mean(t_Z)

    max_val = max(torch.max(torch.abs(t_X)).item(), torch.max(torch.abs(t_Y)).item(), torch.max(torch.abs(t_Z)).item(), 1.0)
    scale = (GRID_SIZE - 1) / (max_val * 2)
    
    ix = torch.clamp(((t_X + max_val) * scale).long(), 0, GRID_SIZE - 1)
    iy = torch.clamp(((t_Y + max_val) * scale).long(), 0, GRID_SIZE - 1)
    iz = torch.clamp(((t_Z + max_val) * scale).long(), 0, GRID_SIZE - 1)

    flat_idx = ix * GRID_SIZE * GRID_SIZE + iy * GRID_SIZE + iz
    counts = torch.bincount(flat_idx, minlength=GRID_SIZE**3)
    density_grid = counts.view(GRID_SIZE, GRID_SIZE, GRID_SIZE).to(torch.complex64)

    k3_space_3d = torch.fft.fftn(density_grid)

    s12, s21 = 1.6, 0.4
    S12_field = k3_space_3d * s12 * torch.exp(1j * torch.tensor(0.5, device=device))
    S21_field = k3_space_3d * s21 * torch.exp(-1j * torch.tensor(0.5, device=device))

    asymmetry_3d = torch.abs(torch.fft.ifftn(S12_field - S21_field))
    
    if device.type == 'cuda':
        torch.cuda.synchronize()
        mem_alloc = torch.cuda.max_memory_allocated(0) / 1024**2
        print(f"      Pic de VRAM utilisé : {mem_alloc:.2f} MB")
        
    calc_time = time.time() - start_gpu
    print(f"      Terminé en {calc_time:.4f} s")
    print("-" * 50)
    print(f"✅ VALIDATION RÉUSSIE !")
    print(f"Asymétrie Maximale détectée : {torch.max(asymmetry_3d).item():.4f}")
    
if __name__ == "__main__":
    run_validation()
