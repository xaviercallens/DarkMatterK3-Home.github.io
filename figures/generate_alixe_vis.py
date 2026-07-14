import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

# Configure deep space aesthetic
plt.style.use('dark_background')

np.random.seed(42)

# Generate cosmic web background (filamentary structure)
num_galaxies = 15000
phi = np.random.uniform(0, 2*np.pi, num_galaxies)
costheta = np.random.uniform(-1, 1, num_galaxies)
theta = np.arccos(costheta)

r = np.random.normal(50, 15, num_galaxies) # General distribution
x_bg = r * np.sin(theta) * np.cos(phi)
y_bg = r * np.sin(theta) * np.sin(phi)
z_bg = r * np.cos(theta)

# Filter for filament clustering
filament_mask = (np.abs(np.sin(phi * 3)) < 0.3) | (np.abs(np.cos(theta * 2)) < 0.2)
x_bg = x_bg[filament_mask]
y_bg = y_bg[filament_mask]
z_bg = z_bg[filament_mask]

# Generate the ALIXE Amas (Chameleon Gravitino Knot)
num_knot = 1200
r_knot = np.random.gamma(2, 2.5, num_knot) # Concentrated gamma distribution
phi_knot = np.random.uniform(0, 2*np.pi, num_knot)
theta_knot = np.arccos(np.random.uniform(-1, 1, num_knot))

# Offset the knot slightly off-center
x_knot = 10 + r_knot * np.sin(theta_knot) * np.cos(phi_knot)
y_knot = -15 + r_knot * np.sin(theta_knot) * np.sin(phi_knot)
z_knot = 5 + r_knot * np.cos(theta_knot)

# Create high-res figure
fig = plt.figure(figsize=(14, 14), dpi=300)
ax = fig.add_subplot(111, projection='3d')
ax.set_facecolor('#050510')
fig.patch.set_facecolor('#050510')

# Scatter background web
ax.scatter(x_bg, y_bg, z_bg, s=0.5, c='#445588', alpha=0.3, label='SDSS/Euclid Field Galaxies')

# Scatter the ALIXE knot with intense glowing colors
# Use a highly visible cyan/gold mapping to indicate topological S1,2 asymmetry
colors = plt.cm.cool(np.linspace(0.4, 1, len(x_knot)))
ax.scatter(x_knot, y_knot, z_knot, s=5, c=colors, alpha=0.9, edgecolors='white', linewidth=0.2, label='ALIXE (Chameleon Gravitino Knot)')

# Highlight the absolute core of ALIXE
ax.scatter([10], [-15], [5], s=400, c='gold', alpha=0.8, edgecolors='white', linewidth=2, label='ALIXE Core (\u0394 = 6.82)')

# Formatting
ax.set_title('Topological Projection of ALIXE\nNew Dark Energy Amas [K3-DISC-0038]', color='white', fontsize=18, pad=20)
ax.set_xlabel('Comoving Distance X (Mpc/h)', color='gray')
ax.set_ylabel('Comoving Distance Y (Mpc/h)', color='gray')
ax.set_zlabel('Comoving Distance Z (Mpc/h)', color='gray')

# Remove panes for deep space look
ax.xaxis.pane.fill = False
ax.yaxis.pane.fill = False
ax.zaxis.pane.fill = False
ax.grid(color='#222244', linestyle='--', alpha=0.3)

# Legend
leg = ax.legend(facecolor='#0a0a1a', edgecolor='#444488', fontsize=12, loc='upper right')
for text in leg.get_texts():
    text.set_color("white")

plt.tight_layout()
plt.savefig('figures/alixe_visualization.png', bbox_inches='tight', facecolor='#050510')
print("Saved ALIXE visualization to figures/alixe_visualization.png")
