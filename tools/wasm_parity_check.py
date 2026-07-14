import os
import json
import time
import subprocess
import torch
import numpy as np

GRID_SIZE = 128
device = torch.device('cpu') # For parity, ensure CPU to avoid precision diffs from CUDA

def compute_python_parity(X, Y, Z, s12, s21):
    t_X = torch.tensor(X, device=device)
    t_Y = torch.tensor(Y, device=device)
    t_Z = torch.tensor(Z, device=device)
    
    # Centrage des données
    t_X = t_X - torch.mean(t_X)
    t_Y = t_Y - torch.mean(t_Y)
    t_Z = t_Z - torch.mean(t_Z)
    
    # Projection des coordonnées sur la grille de densité complexe
    density_grid = torch.zeros((GRID_SIZE, GRID_SIZE, GRID_SIZE), device=device, dtype=torch.complex64)
    
    max_val = max(torch.max(torch.abs(t_X)).item(), torch.max(torch.abs(t_Y)).item(), torch.max(torch.abs(t_Z)).item(), 1.0)
    scale = (GRID_SIZE - 1) / (max_val * 2)
    ix = torch.clamp(((t_X + max_val) * scale).long(), 0, GRID_SIZE - 1)
    iy = torch.clamp(((t_Y + max_val) * scale).long(), 0, GRID_SIZE - 1)
    iz = torch.clamp(((t_Z + max_val) * scale).long(), 0, GRID_SIZE - 1)
    
    flat_idx = ix * GRID_SIZE * GRID_SIZE + iy * GRID_SIZE + iz
    counts = torch.bincount(flat_idx, minlength=GRID_SIZE**3)
    density_grid = counts.view(GRID_SIZE, GRID_SIZE, GRID_SIZE).to(torch.complex64)
    
    # Transformée de Fourier Rapide 3D pour projeter sur la variété K3
    k3_space_3d = torch.fft.fftn(density_grid)
    
    S12_field = k3_space_3d * s12 * torch.exp(1j * torch.tensor(0.5, device=device))
    S21_field = k3_space_3d * s21 * torch.exp(-1j * torch.tensor(0.5, device=device))
    
    # Calcul de la brisure de symétrie
    asymmetry_3d = torch.abs(torch.fft.ifftn(S12_field - S21_field))
    
    mean_asymmetry = torch.mean(asymmetry_3d).item()
    max_asymmetry = torch.max(asymmetry_3d).item()
    delta = abs(s12 - s21)
    
    return mean_asymmetry, max_asymmetry, delta

def main():
    print("Generating synthetic 10,000 galaxy chunk...")
    np.random.seed(42)
    num_galaxies = 10000
    
    # Generate some random comoving coordinates for testing
    X = np.random.uniform(-100.0, 100.0, num_galaxies).astype(np.float32)
    Y = np.random.uniform(-100.0, 100.0, num_galaxies).astype(np.float32)
    Z = np.random.uniform(-100.0, 100.0, num_galaxies).astype(np.float32)

    coords = [{"x": float(x), "y": float(y), "z": float(z)} for x, y, z in zip(X, Y, Z)]
    
    s12 = 1.6
    s21 = 0.5
    
    print("Computing Python reference...")
    start_time = time.time()
    py_mean, py_max, py_delta = compute_python_parity(X, Y, Z, s12, s21)
    py_time = time.time() - start_time
    print(f"Python: Mean={py_mean:.6f}, Max={py_max:.6f}, Delta={py_delta:.6f} in {py_time:.4f}s")
    
    print("Building WASM module...")
    # Build WASM for nodejs target
    # Adjust this command if you are running it manually
    subprocess.run(["wasm-pack", "build", "../core_wasm", "--target", "nodejs"], check=True)
    
    print("Running WASM implementation via Node.js...")
    input_data = {
        "coords": coords,
        "s12": s12,
        "s21": s21
    }
    
    start_time = time.time()
    process = subprocess.run(["node", "run_wasm.js"], input=json.dumps(input_data), capture_output=True, text=True, check=True)
    wasm_time = time.time() - start_time
    
    result = json.loads(process.stdout.strip())
    if result.get("status") != "success":
        print(f"WASM error: {result}")
        return
        
    wasm_mean = float(result["mean_asymmetry"])
    wasm_max = float(result["max_asymmetry"])
    wasm_delta = float(result["delta"])
    
    print(f"WASM:   Mean={wasm_mean:.6f}, Max={wasm_max:.6f}, Delta={wasm_delta:.6f} in {wasm_time:.4f}s")
    
    mean_diff = abs(py_mean - wasm_mean)
    max_diff = abs(py_max - wasm_max)
    
    print(f"\nDifferences:\nMean Diff: {mean_diff:.8f}\nMax Diff: {max_diff:.8f}")
    
    if mean_diff < 1e-4 and max_diff < 1e-4:
        print("\n✅ PARITY CHECK PASSED")
    else:
        print("\n❌ PARITY CHECK FAILED")

if __name__ == "__main__":
    main()
