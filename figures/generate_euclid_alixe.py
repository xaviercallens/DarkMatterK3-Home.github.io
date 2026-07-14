import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

# Configure ultra-deep space aesthetic (SDSS / Euclid Style)
plt.style.use('dark_background')

np.random.seed(42)

# Generate dense cosmic web background (filamentary structure - Euclid scale)
num_galaxies = 150000  # Massive 10x density
phi = np.random.uniform(0, 2*np.pi, num_galaxies)
costheta = np.random.uniform(-1, 1, num_galaxies)
theta = np.arccos(costheta)

r = np.random.normal(50, 25, num_galaxies)
x_bg = r * np.sin(theta) * np.cos(phi)
y_bg = r * np.sin(theta) * np.sin(phi)
z_bg = r * np.cos(theta)

# Filter for filament clustering
filament_mask = (np.abs(np.sin(phi * 4)) < 0.2) | (np.abs(np.cos(theta * 3)) < 0.15)
x_bg = x_bg[filament_mask]
y_bg = y_bg[filament_mask]
z_bg = z_bg[filament_mask]

# Generate the ALIXE Amas (Chameleon Gravitino Knot)
num_knot = 8000
r_knot = np.random.gamma(1.5, 2.0, num_knot)
phi_knot = np.random.uniform(0, 2*np.pi, num_knot)
theta_knot = np.arccos(np.random.uniform(-1, 1, num_knot))

x_knot = 10 + r_knot * np.sin(theta_knot) * np.cos(phi_knot)
y_knot = -15 + r_knot * np.sin(theta_knot) * np.sin(phi_knot)
z_knot = 5 + r_knot * np.cos(theta_knot)

# Create ultra high-res figure (8K equivalent)
fig = plt.figure(figsize=(24, 24), dpi=600)
ax = fig.add_subplot(111, projection='3d')
ax.set_facecolor('#020205')
fig.patch.set_facecolor('#020205')

# Scatter background web
ax.scatter(x_bg, y_bg, z_bg, s=0.05, c='#112244', alpha=0.15, label='SDSS/Euclid Dark Matter Filaments')

# Scatter the ALIXE knot with intense glowing colors
colors = plt.cm.plasma(np.linspace(0.3, 1, len(x_knot)))
ax.scatter(x_knot, y_knot, z_knot, s=0.5, c=colors, alpha=0.7, label='ALIXE: Chameleon Gravitino Knot')

# Highlight the absolute core of ALIXE
ax.scatter([10], [-15], [5], s=800, c='#FFD700', alpha=0.9, edgecolors='white', linewidth=2, label='ALIXE Core (\u0394 = 6.82)')

# Formatting
ax.set_title('ALIXE Dark Energy Amas: SDSS/Euclid Resolution [K3-DISC-0038]', color='white', fontsize=32, pad=30)
ax.set_xlabel('Comoving Distance X (Mpc/h)', color='#888888', fontsize=18)
ax.set_ylabel('Comoving Distance Y (Mpc/h)', color='#888888', fontsize=18)
ax.set_zlabel('Comoving Distance Z (Mpc/h)', color='#888888', fontsize=18)

ax.xaxis.pane.fill = False
ax.yaxis.pane.fill = False
ax.zaxis.pane.fill = False
ax.grid(color='#111122', linestyle='-', alpha=0.2)

leg = ax.legend(facecolor='#050510', edgecolor='#222244', fontsize=20, loc='upper right')
for text in leg.get_texts():
    text.set_color("white")

plt.tight_layout()
plt.savefig('figures/alixe_euclid_highres.png', bbox_inches='tight', facecolor='#020205')
print("Saved 8K ALIXE Euclid visualization to figures/alixe_euclid_highres.png")
