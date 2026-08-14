"""
Part C - Advanced Challenge: 3D Zero-Gravity Space Station Robotic Arm
=======================================================================
Description:
Kinematic design, trajectory planning, and 6-DOF Damped Least Squares (DLS)
Inverse Kinematics simulation for a 3D Space Station Manipulator Arm operating 
in a zero-gravity environment. Performs precise 3D positioning and orientation alignment 
to capture and reposition equipment modules.

Author: Robotics Engineering Assistant
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os

class SpaceStationArm6DOF:
    """6-DOF Articulated Spatial Manipulator for Microgravity Operations."""
    def __init__(self):
        # Link lengths (meters) - Large space station arm scale
        self.link_lengths = [2.5, 3.0, 2.5, 1.2, 0.8, 0.5]
        
        # Initial Joint Angles (radians)
        self.q = np.array([0.1, 0.4, -0.6, 0.2, 0.5, 0.0])
        
    def rotation_matrix_x(self, angle):
        c, s = np.cos(angle), np.sin(angle)
        return np.array([[1, 0, 0], [0, c, -s], [0, s, c]])

    def rotation_matrix_y(self, angle):
        c, s = np.cos(angle), np.sin(angle)
        return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])

    def rotation_matrix_z(self, angle):
        c, s = np.cos(angle), np.sin(angle)
        return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])

    def euler_to_rotation_matrix(self, roll, pitch, yaw):
        """Computes 3x3 rotation matrix from Roll (X), Pitch (Y), Yaw (Z)."""
        R_x = self.rotation_matrix_x(roll)
        R_y = self.rotation_matrix_y(pitch)
        R_z = self.rotation_matrix_z(yaw)
        return R_z @ R_y @ R_x

    def rotation_matrix_to_euler(self, R):
        """Extracts Roll, Pitch, Yaw from rotation matrix R."""
        sy = np.sqrt(R[0, 0]**2 + R[1, 0]**2)
        singular = sy < 1e-6
        if not singular:
            roll = np.arctan2(R[2, 1], R[2, 2])
            pitch = np.arctan2(-R[2, 0], sy)
            yaw = np.arctan2(R[1, 0], R[0, 0])
        else:
            roll = np.arctan2(-R[1, 2], R[1, 1])
            pitch = np.arctan2(-R[2, 0], sy)
            yaw = 0.0
        return np.array([roll, pitch, yaw])

    def forward_kinematics(self, q=None):
        """Calculates 3D joint transformations and end-effector pose."""
        if q is None:
            q = self.q

        l1, l2, l3, l4, l5, l6 = self.link_lengths
        
        # Homogeneous transformations for spatial 6-DOF arm
        T = np.eye(4)
        positions = [T[:3, 3].copy()]
        orientations = [T[:3, :3].copy()]
        
        # Joint 1: Base Yaw (Z-axis rotation)
        R1 = self.rotation_matrix_z(q[0])
        T1 = np.eye(4)
        T1[:3, :3] = R1
        T1[:3, 3] = [0, 0, l1]
        T = T @ T1
        positions.append(T[:3, 3].copy())
        orientations.append(T[:3, :3].copy())
        
        # Joint 2: Shoulder Pitch (Y-axis rotation)
        R2 = self.rotation_matrix_y(q[1])
        T2 = np.eye(4)
        T2[:3, :3] = R2
        T2[:3, 3] = [l2 * np.sin(q[1]), 0, l2 * np.cos(q[1])]
        T = T @ T2
        positions.append(T[:3, 3].copy())
        orientations.append(T[:3, :3].copy())
        
        # Joint 3: Elbow Pitch (Y-axis rotation)
        R3 = self.rotation_matrix_y(q[2])
        T3 = np.eye(4)
        T3[:3, :3] = R3
        T3[:3, 3] = [l3 * np.sin(q[2]), 0, l3 * np.cos(q[2])]
        T = T @ T3
        positions.append(T[:3, 3].copy())
        orientations.append(T[:3, :3].copy())
        
        # Joint 4: Wrist Roll (X-axis rotation)
        R4 = self.rotation_matrix_x(q[3])
        T4 = np.eye(4)
        T4[:3, :3] = R4
        T4[:3, 3] = [0, 0, l4]
        T = T @ T4
        positions.append(T[:3, 3].copy())
        orientations.append(T[:3, :3].copy())
        
        # Joint 5: Wrist Pitch (Y-axis rotation)
        R5 = self.rotation_matrix_y(q[4])
        T5 = np.eye(4)
        T5[:3, :3] = R5
        T5[:3, 3] = [0, 0, l5]
        T = T @ T5
        positions.append(T[:3, 3].copy())
        orientations.append(T[:3, :3].copy())
        
        # Joint 6: Wrist Yaw (Z-axis rotation / End effector tool)
        R6 = self.rotation_matrix_z(q[5])
        T6 = np.eye(4)
        T6[:3, :3] = R6
        T6[:3, 3] = [0, 0, l6]
        T = T @ T6
        positions.append(T[:3, 3].copy())
        orientations.append(T[:3, :3].copy())
        
        return positions, T

    def compute_numerical_jacobian(self, q, delta=1e-5):
        """Computes 6x6 geometric Jacobian numerically."""
        J = np.zeros((6, 6))
        pos0, T0 = self.forward_kinematics(q)
        p0 = T0[:3, 3]
        r0 = T0[:3, :3]
        e0 = self.rotation_matrix_to_euler(r0)
        
        for i in range(6):
            q_step = q.copy()
            q_step[i] += delta
            pos_step, T_step = self.forward_kinematics(q_step)
            p_step = T_step[:3, 3]
            r_step = T_step[:3, :3]
            e_step = self.rotation_matrix_to_euler(r_step)
            
            dp = (p_step - p0) / delta
            de = (e_step - e0) / delta
            # Handle euler wraparound
            de = np.arctan2(np.sin(de), np.cos(de))
            
            J[:3, i] = dp
            J[3:, i] = de
            
        return J

    def inverse_kinematics_dls(self, target_pos, target_rpy, max_iter=150, tol=1e-4, damping=0.08):
        """
        Solves 6D Inverse Kinematics using Damped Least Squares (DLS).
        Prevents joint velocity singularities in space teleoperation.
        """
        q_curr = self.q.copy()
        pos_errors = []
        ori_errors = []
        
        target_R = self.euler_to_rotation_matrix(*target_rpy)
        
        for step in range(max_iter):
            positions, T_curr = self.forward_kinematics(q_curr)
            curr_pos = T_curr[:3, 3]
            curr_R = T_curr[:3, :3]
            
            # Position error
            pos_err = target_pos - curr_pos
            
            # Orientation error vector using rotation matrix error R_err = R_target * R_curr^T
            R_err = target_R @ curr_R.T
            # Convert R_err to axis-angle error vector
            angle = np.arccos(np.clip((np.trace(R_err) - 1.0) / 2.0, -1.0, 1.0))
            if abs(angle) < 1e-5:
                ori_err = np.zeros(3)
            else:
                axis = np.array([R_err[2, 1] - R_err[1, 2],
                                 R_err[0, 2] - R_err[2, 0],
                                 R_err[1, 0] - R_err[0, 1]]) / (2.0 * np.sin(angle))
                ori_err = axis * angle
                
            error_vector = np.concatenate([pos_err, ori_err])
            
            pos_err_norm = np.linalg.norm(pos_err)
            ori_err_norm = np.linalg.norm(ori_err)
            
            pos_errors.append(pos_err_norm)
            ori_errors.append(ori_err_norm)
            
            if pos_err_norm < tol and ori_err_norm < tol:
                print(f"[+] IK Converged at iteration {step}! Pos Err: {pos_err_norm:.6f}m, Ori Err: {ori_err_norm:.6f}rad")
                break
                
            # DLS Jacobian pseudo-inverse
            J = self.compute_numerical_jacobian(q_curr)
            # Damping matrix lambda^2 * I
            J_dls = J.T @ np.linalg.inv(J @ J.T + (damping**2) * np.eye(6))
            
            dq = J_dls @ error_vector
            q_curr += dq * 0.5  # Step size scaling for smooth update
            
        self.q = q_curr
        return q_curr, pos_errors, ori_errors


def run_space_station_simulation():
    """Runs 3D Space Station Manipulator Simulation and visualization."""
    print("=" * 65)
    print("   PART C: 3D SPACE STATION ROBOTIC ARM (ZERO-GRAVITY SIMULATION)   ")
    print("=" * 65)
    
    arm = SpaceStationArm6DOF()
    
    # Target 3D pose in Space Station reference frame (x, y, z) + (roll, pitch, yaw)
    target_position = np.array([3.5, 2.2, 4.0])  # Target payload module grapple fixture
    target_rpy = np.array([np.radians(30), np.radians(45), np.radians(-20)]) # Required alignment
    
    print("[*] Target Grapple Location (m)  :", target_position)
    print("[*] Target Orientation RPY (deg) :", np.degrees(target_rpy))
    print("[*] Running Damped Least Squares (DLS) Inverse Kinematics...")
    
    final_q, pos_errs, ori_errs = arm.inverse_kinematics_dls(target_position, target_rpy)
    final_positions, final_T = arm.forward_kinematics(final_q)
    end_effector_pos = final_T[:3, 3]
    
    print("\n--- IK SOLUTION RESULTS ---")
    print(f"Final Joint Angles (rad) : {np.round(final_q, 4)}")
    print(f"Final End-Effector Pos   : {np.round(end_effector_pos, 4)}")
    print(f"Position Error           : {pos_errs[-1]:.6f} m")
    print(f"Orientation Error        : {ori_errs[-1]:.6f} rad")
    
    # Create 3D Plot + Error Convergence Charts
    fig = plt.figure(figsize=(16, 7.5))
    
    # --- Subplot 1: 3D Space Station & Robotic Arm ---
    ax3d = fig.add_subplot(1, 2, 1, projection='3d')
    ax3d.set_title("3D Space Station Robotic Arm (Zero-Gravity Target Alignment)", fontsize=12, fontweight='bold')
    
    # Draw Space Station Truss Structure (Reference backdrop)
    truss_x = [0, 0, 0, 0, 0]
    truss_y = [-2, 4, 4, -2, -2]
    truss_z = [0, 0, -2, -2, 0]
    ax3d.plot(truss_x, truss_y, truss_z, 'gray', linestyle='--', linewidth=2, label='Space Station Module Truss')
    
    # Draw Payload Target Box
    tx, ty, tz = target_position
    ax3d.scatter([tx], [ty], [tz], color='gold', s=120, marker='*', label='Payload Grapple Target')
    
    # Draw Arm Links
    px = [p[0] for p in final_positions]
    py = [p[1] for p in final_positions]
    pz = [p[2] for p in final_positions]
    
    ax3d.plot(px, py, pz, '-o', color='#0275d8', linewidth=4, markersize=8, label='6-DOF Robotic Arm Links')
    ax3d.scatter([px[0]], [py[0]], [pz[0]], color='black', s=100, label='Base Mounting Joint')
    ax3d.scatter([px[-1]], [py[-1]], [pz[-1]], color='red', s=100, label='End-Effector Wrist')
    
    # Draw End-Effector Orientation Frame Vector
    target_R = arm.euler_to_rotation_matrix(*target_rpy)
    vector_len = 1.0
    x_dir = target_R @ np.array([vector_len, 0, 0])
    y_dir = target_R @ np.array([0, vector_len, 0])
    z_dir = target_R @ np.array([0, 0, vector_len])
    
    ax3d.quiver(tx, ty, tz, x_dir[0], x_dir[1], x_dir[2], color='r', length=0.8, normalize=True, label='Target Tool X-axis')
    ax3d.quiver(tx, ty, tz, y_dir[0], y_dir[1], y_dir[2], color='g', length=0.8, normalize=True, label='Target Tool Y-axis')
    ax3d.quiver(tx, ty, tz, z_dir[0], z_dir[1], z_dir[2], color='b', length=0.8, normalize=True, label='Target Tool Z-axis')
    
    ax3d.set_xlabel('X (m)')
    ax3d.set_ylabel('Y (m)')
    ax3d.set_zlabel('Z (m)')
    ax3d.legend(loc='upper left', fontsize=9)
    
    # --- Subplot 2: IK Error Convergence Curves ---
    ax_err = fig.add_subplot(1, 2, 2)
    iters = range(len(pos_errs))
    
    ax_err.plot(iters, pos_errs, 'b-', linewidth=2, label='Position Error (m)')
    ax_err.plot(iters, ori_errs, 'r--', linewidth=2, label='Orientation Error (rad)')
    ax_err.set_yscale('log')
    ax_err.set_title("Inverse Kinematics Convergence Performance", fontsize=12, fontweight='bold')
    ax_err.set_xlabel("Solver Iteration Step", fontsize=11)
    ax_err.set_ylabel("Error Magnitude (Log Scale)", fontsize=11)
    ax_err.grid(True, which="both", linestyle=':', alpha=0.7)
    ax_err.legend(loc='upper right', fontsize=11)
    
    stats_text = (f"Space Station Arm Performance:\n"
                  f"• DoF: 6 (Rotational)\n"
                  f"• DLS Damping λ: 0.08\n"
                  f"• Converged Iterations: {len(pos_errs)}\n"
                  f"• Final Pos Error: {pos_errs[-1]:.2e} m\n"
                  f"• Final Ori Error: {ori_errs[-1]:.2e} rad")
    ax_err.text(0.05, 0.05, stats_text, transform=ax_err.transAxes, fontsize=10,
                bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.9, edgecolor='orange'))

    output_img = os.path.join(os.path.dirname(__file__), "part_c_space_station_3d_arm_result.png")
    plt.tight_layout()
    plt.savefig(output_img, dpi=300)
    print(f"[+] Saved 3D Space Station Arm plot image to: {output_img}")
    plt.close()
    
    print("=" * 65)
    print("Part C Simulation Completed Successfully!\n")

if __name__ == "__main__":
    run_space_station_simulation()
