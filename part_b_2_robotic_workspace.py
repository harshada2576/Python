"""
Part B - Task 2: Robotic Workspace Reachable Points Visualization
==================================================================
Description:
Computes and visualizes the reachable workspace of a 3-DOF articulated robotic arm
using Monte Carlo forward kinematics sampling and Yoshikawa's Manipulability Index.

Author: Robotics Engineering Assistant
"""

import numpy as np
import matplotlib.pyplot as plt
import os

class RoboticArm3DOF:
    """3-DOF Planar Articulated Robot Arm Kinematics & Dexterity Evaluator."""
    def __init__(self, l1=1.2, l2=1.0, l3=0.8,
                 theta1_lim=(-np.pi, np.pi),
                 theta2_lim=(-np.radians(135), np.radians(135)),
                 theta3_lim=(-np.radians(150), np.radians(150))):
        self.l1 = l1
        self.l2 = l2
        self.l3 = l3
        self.link_lengths = [l1, l2, l3]
        
        self.lim1 = theta1_lim
        self.lim2 = theta2_lim
        self.lim3 = theta3_lim

    def forward_kinematics(self, t1, t2, t3):
        """Calculates joint coordinates (x, y) for all links."""
        t12 = t1 + t2
        t123 = t1 + t2 + t3
        
        x0, y0 = 0.0, 0.0
        x1 = x0 + self.l1 * np.cos(t1)
        y1 = y0 + self.l1 * np.sin(t1)
        
        x2 = x1 + self.l2 * np.cos(t12)
        y2 = y1 + self.l2 * np.sin(t12)
        
        x3 = x2 + self.l3 * np.cos(t123)
        y3 = y2 + self.l3 * np.sin(t123)
        
        return [(x0, y0), (x1, y1), (x2, y2), (x3, y3)]

    def end_effector_pos(self, t1, t2, t3):
        """Calculates end-effector (x, y) coordinates."""
        t12 = t1 + t2
        t123 = t1 + t2 + t3
        x = self.l1 * np.cos(t1) + self.l2 * np.cos(t12) + self.l3 * np.cos(t123)
        y = self.l1 * np.sin(t1) + self.l2 * np.sin(t12) + self.l3 * np.sin(t123)
        return x, y

    def jacobian(self, t1, t2, t3):
        """Calculates 2x3 position Jacobian matrix."""
        t12 = t1 + t2
        t123 = t1 + t2 + t3
        
        s1 = np.sin(t1)
        c1 = np.cos(t1)
        s12 = np.sin(t12)
        c12 = np.cos(t12)
        s123 = np.sin(t123)
        c123 = np.cos(t123)
        
        j11 = -self.l1*s1 - self.l2*s12 - self.l3*s123
        j12 = -self.l2*s12 - self.l3*s123
        j13 = -self.l3*s123
        
        j21 = self.l1*c1 + self.l2*c12 + self.l3*c123
        j22 = self.l2*c12 + self.l3*c123
        j23 = self.l3*c123
        
        return np.array([[j11, j12, j13],
                         [j21, j22, j23]])

    def manipulability(self, t1, t2, t3):
        """Calculates Yoshikawa's Manipulability Index w = sqrt(det(J * J^T))."""
        J = self.jacobian(t1, t2, t3)
        JJt = J @ J.T
        det_val = np.linalg.det(JJt)
        return np.sqrt(max(0.0, det_val))

    def sample_workspace(self, num_samples=30000):
        """Performs Monte Carlo sampling over joint angle space."""
        t1_samples = np.random.uniform(self.lim1[0], self.lim1[1], num_samples)
        t2_samples = np.random.uniform(self.lim2[0], self.lim2[1], num_samples)
        t3_samples = np.random.uniform(self.lim3[0], self.lim3[1], num_samples)
        
        t12 = t1_samples + t2_samples
        t123 = t12 + t3_samples
        
        x = self.l1 * np.cos(t1_samples) + self.l2 * np.cos(t12) + self.l3 * np.cos(t123)
        y = self.l1 * np.sin(t1_samples) + self.l2 * np.sin(t12) + self.l3 * np.sin(t123)
        
        # Calculate manipulability for all points
        manipulabilities = np.zeros(num_samples)
        for i in range(num_samples):
            manipulabilities[i] = self.manipulability(t1_samples[i], t2_samples[i], t3_samples[i])
            
        return x, y, manipulabilities, (t1_samples, t2_samples, t3_samples)


def visualize_workspace():
    """Generates workspace scatter plot and arm configuration overlays."""
    print("=" * 60)
    print("     PART B - TASK 2: ROBOTIC WORKSPACE VISUALIZATION     ")
    print("=" * 60)
    
    arm = RoboticArm3DOF(l1=1.2, l2=1.0, l3=0.8)
    num_samples = 35000
    print(f"[*] Link Lengths      : L1={arm.l1}m, L2={arm.l2}m, L3={arm.l3}m")
    print(f"[*] Max Reach Radius  : {arm.l1 + arm.l2 + arm.l3:.2f} meters")
    print(f"[*] Sampling Count    : {num_samples:,} configurations (Monte Carlo)")
    
    x, y, w_indices, joint_samples = arm.sample_workspace(num_samples=num_samples)
    r_distances = np.hypot(x, y)
    
    r_max = np.max(r_distances)
    r_min = np.min(r_distances)
    
    # Estimate workspace area using convex hull / radial ring integration
    max_theoretical_reach = arm.l1 + arm.l2 + arm.l3
    min_theoretical_reach = max(0.0, arm.l1 - arm.l2 - arm.l3)
    workspace_area = np.pi * (r_max**2 - r_min**2)
    
    print(f"[+] Empirical Max Outer Reach Radius : {r_max:.4f} m")
    print(f"[+] Empirical Min Inner Bound Radius : {r_min:.4f} m")
    print(f"[+] Estimated Reachable Workspace Area: {workspace_area:.4f} m²")
    print(f"[+] Peak Manipulability Index        : {np.max(w_indices):.4f}")
    
    # Create Figure with 2 Subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7.5))
    
    # --- Subplot 1: Reachable Workspace Scatter Map ---
    sc = ax1.scatter(x, y, c=w_indices, cmap='viridis', s=1.5, alpha=0.6)
    cbar = fig.colorbar(sc, ax=ax1, label="Yoshikawa Manipulability Index w")
    
    # Draw reach boundaries
    outer_circle = plt.Circle((0, 0), max_theoretical_reach, fill=False, color='red', linestyle='--', linewidth=1.8, label=f'Max Reach Boundary ({max_theoretical_reach:.1f}m)')
    ax1.add_patch(outer_circle)
    
    ax1.plot(0, 0, 'k+', markersize=12, markeredgewidth=2, label='Base Joint (0,0)')
    ax1.set_aspect('equal')
    ax1.set_xlim(-3.5, 3.5)
    ax1.set_ylim(-3.5, 3.5)
    ax1.set_title("Reachable Workspace Density & Manipulability Heatmap", fontsize=12, fontweight='bold')
    ax1.set_xlabel("X (meters)", fontsize=11)
    ax1.set_ylabel("Y (meters)", fontsize=11)
    ax1.grid(True, linestyle=':', alpha=0.7)
    ax1.legend(loc='upper right')
    
    # --- Subplot 2: Robot Configurations Overlaid ---
    ax2.set_aspect('equal')
    ax2.set_xlim(-3.5, 3.5)
    ax2.set_ylim(-3.5, 3.5)
    ax2.set_title("Sample Arm Poses Across Workspace Boundaries", fontsize=12, fontweight='bold')
    ax2.set_xlabel("X (meters)", fontsize=11)
    ax2.set_ylabel("Y (meters)", fontsize=11)
    ax2.grid(True, linestyle=':', alpha=0.7)
    
    # Plot background light scatter
    ax2.scatter(x[::5], y[::5], c='lightgrey', s=0.8, alpha=0.3, label='Workspace Boundary')
    
    # Select 3 sample configurations: Max extension, Min extension, High Dexterity
    max_idx = np.argmax(r_distances)
    high_w_idx = np.argmax(w_indices)
    
    t1_samples, t2_samples, t3_samples = joint_samples
    
    configs = [
        ("Max Reach Pose", t1_samples[max_idx], t2_samples[max_idx], t3_samples[max_idx], '#d9534f'),
        ("High Dexterity Pose", t1_samples[high_w_idx], t2_samples[high_w_idx], t3_samples[high_w_idx], '#0275d8'),
        ("Folded Pose", np.radians(45), np.radians(-110), np.radians(90), '#5cb85c')
    ]
    
    for label, t1, t2, t3, color in configs:
        pts = arm.forward_kinematics(t1, t2, t3)
        pxs = [pt[0] for pt in pts]
        pys = [pt[1] for pt in pts]
        
        ax2.plot(pxs, pys, '-o', color=color, linewidth=3, markersize=7, label=label)
        ax2.plot(pxs[-1], pys[-1], 's', color=color, markersize=9)
        
    ax2.plot(0, 0, 'k+', markersize=12, markeredgewidth=2)
    ax2.legend(loc='upper right', frameon=True, shadow=True)
    
    # Annotate Workspace Specs
    stats_box = (f"Workspace Reach Specs:\n"
                 f"• Max Outer Radius: {r_max:.3f} m\n"
                 f"• Min Inner Radius: {r_min:.3f} m\n"
                 f"• Total Area: {workspace_area:.2f} m²\n"
                 f"• Evaluated Poses: {num_samples:,}")
    ax1.text(0.03, 0.03, stats_box, transform=ax1.transAxes, fontsize=10,
             bbox=dict(boxstyle='round', facecolor='white', alpha=0.85, edgecolor='gray'))
    
    output_img = os.path.join(os.path.dirname(__file__), "part_b_2_robotic_workspace_result.png")
    plt.tight_layout()
    plt.savefig(output_img, dpi=300)
    print(f"[+] Saved workspace visualization image to: {output_img}")
    plt.close()
    
    print("=" * 60)
    print("Part B - Task 2 Workspace Plotting Completed Successfully!\n")

if __name__ == "__main__":
    visualize_workspace()
