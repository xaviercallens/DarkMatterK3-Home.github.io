import numpy as np

def compute_beta(denominator):
    mass_vector = np.logspace(8, 14, 15)
    f_b = 0.17
    rc_vector = []
    for M_halo in mass_vector:
        r_grid = np.logspace(-4, 3, 2000)
        z_field = (M_halo ** (0.15 + f_b)) / r_grid
        # We assume the generic form for the map: F(z) = z^2 / (1 + A*z + C*z^2)
        # The user only mentioned C, let's assume A doesn't affect the asymptotic limit much
        # But wait, A is needed. Let's try to just use the asymptotic limit F(z) -> 1/C
        f_vals = (z_field**2) / (1.0 + 10.0 * z_field + denominator * (z_field**2))
        saturation_limit = 0.99 * (1.0 / denominator)
        sat_indices = np.where(f_vals >= saturation_limit)[0]
        if len(sat_indices) > 0:
            r_c = r_grid[sat_indices[-1]]
        else:
            r_c = r_grid[0]
        rc_vector.append(r_c)
        
    log_M = np.log10(mass_vector)
    log_rc = np.log10(rc_vector)
    beta_theory, _ = np.polyfit(log_M, log_rc, 1)
    return beta_theory

for d in range(60, 151, 10):
    print(f"Denominator {d}: beta = {compute_beta(d):.4f}")
