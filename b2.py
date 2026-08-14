import matplotlib.pyplot as plt
import numpy as np

# --- Arm Parameters ---
l1 = 2.5  # Length of link 1 (meters)
l2 = 1.8  # Length of link 2 (meters)

# Joint constraints (in radians)
theta1_range = np.radians([0, 180])  # Base joint limits: 0° to 180°
theta2_range = np.radians([-135, 135])  # Elbow joint limits: -135° to 135°

# --- Sample Joint Space ---
num_samples = 120
t1 = np.linspace(theta1_range[0], theta1_range[1], num_samples)
t2 = np.linspace(theta2_range[0], theta2_range[1], num_samples)

# Grid of all joint angle combinations
T1, T2 = np.meshgrid(t1, t2)

# --- Forward Kinematics Computation ---
# End-effector reachable position (x, y)
X = l1 * np.cos(T1) + l2 * np.cos(T1 + T2)
Y = l1 * np.sin(T1) + l2 * np.sin(T1 + T2)

# Calculate distance from origin for color mapping
R = np.sqrt(X**2 + Y**2)

# --- Plot Workspace ---
fig, ax = plt.subplots(figsize=(9, 7))

# Plot Reachable Point Cloud
scatter = ax.scatter(
    X.flatten(),
    Y.flatten(),
    c=R.flatten(),
    cmap='viridis',
    s=10,
    alpha=0.6,
    label='Reachable Point Cloud',
)
cbar = plt.colorbar(scatter, ax=ax)
cbar.set_label('Reach Distance from Base (meters)')

# Plot Base & Example Arm Configuration
sample_t1, sample_t2 = np.radians(45), np.radians(30)
joint1_x = l1 * np.cos(sample_t1)
joint1_y = l1 * np.sin(sample_t1)
ee_x = joint1_x + l2 * np.cos(sample_t1 + sample_t2)
ee_y = joint1_y + l2 * np.sin(sample_t1 + sample_t2)

# Draw dynamic arm pose
ax.plot(
    [0, joint1_x, ee_x],
    [0, joint1_y, ee_y],
    'r-o',
    linewidth=4,
    markersize=8,
    label='Arm Sample Pose',
)
ax.scatter([0], [0], color='black', s=150, zorder=5, label='Robot Base')

# Formats
ax.set_title(
    'Robotic Arm Workspace Analysis (Reachable Points)', fontsize=13
)
ax.set_xlabel('X Coordinate (m)')
ax.set_ylabel('Y Coordinate (m)')
ax.set_aspect('equal')
ax.legend(loc='upper right')
plt.grid(True, linestyle='--', alpha=0.5)

plt.show()