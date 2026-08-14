"""
Part B - Task 1: Obstacle Detection Robot Simulation
===================================================
Description:
Simulates an autonomous mobile robot equipped with a multi-beam LIDAR sensor array.
The robot navigates through an environment with circular and rectangular obstacles 
to reach a target location using Artificial Potential Field (APF) with reactive 
obstacle avoidance.

Author: Robotics Engineering Assistant
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Polygon
import os

class Obstacle:
    """Represents circular and rectangular obstacles in 2D space."""
    def __init__(self, obs_type, params):
        self.obs_type = obs_type  # 'circle' or 'rect'
        self.params = params      # circle: (cx, cy, r), rect: (x, y, w, h)

    def distance_and_normal(self, point):
        """Calculates distance from a 2D point to the obstacle surface and normal vector."""
        px, py = point
        if self.obs_type == 'circle':
            cx, cy, r = self.params
            dist_to_center = np.hypot(px - cx, py - cy)
            dist = dist_to_center - r
            if dist_to_center > 1e-6:
                normal = np.array([(px - cx) / dist_to_center, (py - cy) / dist_to_center])
            else:
                normal = np.array([1.0, 0.0])
            return max(0.0, dist), normal
        elif self.obs_type == 'rect':
            rx, ry, w, h = self.params
            # Closest point on rectangle boundary
            cx = max(rx, min(px, rx + w))
            cy = max(ry, min(py, ry + h))
            dist = np.hypot(px - cx, py - cy)
            if dist > 1e-6:
                normal = np.array([(px - cx) / dist, (py - cy) / dist])
            else:
                normal = np.array([1.0, 0.0])
            return dist, normal

    def ray_intersection(self, ray_start, ray_angle, max_range):
        """Calculates intersection distance of a ray with the obstacle."""
        ox, oy = ray_start
        dx = np.cos(ray_angle)
        dy = np.sin(ray_angle)

        if self.obs_type == 'circle':
            cx, cy, r = self.params
            # Ray-circle intersection quadratic formula
            fx = ox - cx
            fy = oy - cy
            a = dx*dx + dy*dy
            b = 2 * (fx*dx + fy*dy)
            c = fx*fx + fy*fy - r*r
            discriminant = b*b - 4*a*c
            if discriminant >= 0:
                t1 = (-b - np.sqrt(discriminant)) / (2*a)
                t2 = (-b + np.sqrt(discriminant)) / (2*a)
                if t1 > 1e-3 and t1 <= max_range:
                    return t1
                elif t2 > 1e-3 and t2 <= max_range:
                    return t2
        elif self.obs_type == 'rect':
            rx, ry, w, h = self.params
            # Ray-AABB intersection
            tmin = 0.0
            tmax = max_range
            
            # X slab
            if abs(dx) < 1e-9:
                if ox < rx or ox > rx + w:
                    return max_range
            else:
                t1 = (rx - ox) / dx
                t2 = (rx + w - ox) / dx
                tmin = max(tmin, min(t1, t2))
                tmax = min(tmax, max(t1, t2))

            # Y slab
            if abs(dy) < 1e-9:
                if oy < ry or oy > ry + h:
                    return max_range
            else:
                t1 = (ry - oy) / dy
                t2 = (ry + h - oy) / dy
                tmin = max(tmin, min(t1, t2))
                tmax = min(tmax, max(t1, t2))

            if tmax >= tmin and tmin > 1e-3:
                return tmin

        return max_range


class ObstacleDetectionRobot:
    """Mobile Robot with LIDAR Sensor Array and APF Steering."""
    def __init__(self, start_pos=(2.0, 2.0), goal_pos=(18.0, 18.0)):
        self.pos = np.array(start_pos, dtype=float)
        self.goal = np.array(goal_pos, dtype=float)
        self.heading = np.arctan2(self.goal[1] - self.pos[1], self.goal[0] - self.pos[0])
        self.radius = 0.5  # Robot size
        
        # Sensor specs
        self.num_rays = 36  # 360 degree scanner with 10 degree resolution
        self.max_range = 5.0
        self.sensor_angles = np.linspace(0, 2*np.pi, self.num_rays, endpoint=False)
        
        # Motion parameters
        self.v_max = 0.4
        self.w_max = np.radians(45) # max turn rate
        self.dt = 0.1
        
        # Trajectory history
        self.path_x = [self.pos[0]]
        self.path_y = [self.pos[1]]
        self.scan_hits = []

    def scan_environment(self, obstacles):
        """Performs LIDAR ray-casting across all sensors."""
        readings = []
        hits = []
        for angle in self.sensor_angles:
            global_angle = self.heading + angle
            min_dist = self.max_range
            hit_point = None
            
            for obs in obstacles:
                d = obs.ray_intersection(self.pos, global_angle, self.max_range)
                if d < min_dist:
                    min_dist = d
                    hit_point = (self.pos[0] + d * np.cos(global_angle),
                                 self.pos[1] + d * np.sin(global_angle))
            
            readings.append(min_dist)
            hits.append((hit_point, global_angle, min_dist))
        
        self.scan_hits = hits
        return readings

    def compute_apf_velocity(self, readings, obstacles):
        """Calculates linear and angular velocities using APF and LIDAR data."""
        # 1. Goal attraction force
        dist_to_goal = np.linalg.norm(self.goal - self.pos)
        k_att = 1.0
        f_att = k_att * (self.goal - self.pos) / max(dist_to_goal, 1.0)
        
        # 2. Obstacle repulsive force from LIDAR readings
        f_rep = np.array([0.0, 0.0])
        k_rep = 2.5
        d_zero = 3.0  # Threshold distance of influence
        
        for dist, (hit_pt, angle, _) in zip(readings, self.scan_hits):
            if dist < d_zero and dist > 0.05:
                # Direction from obstacle hit point to robot
                obs_vec = np.array([np.cos(angle), np.sin(angle)])
                # Repulsive magnitude
                mag = k_rep * ((1.0 / dist) - (1.0 / d_zero)) * (1.0 / (dist**2))
                f_rep -= mag * obs_vec  # Push away from obstacle
                
        # Total force
        f_total = f_att + f_rep
        
        # Target heading from force vector
        target_heading = np.arctan2(f_total[1], f_total[0])
        
        # Angular velocity control
        heading_err = np.arctan2(np.sin(target_heading - self.heading), 
                                 np.cos(target_heading - self.heading))
        w = np.clip(2.0 * heading_err, -self.w_max, self.w_max)
        
        # Linear velocity control (slow down when turning sharply or close to obstacles)
        min_obs_dist = min(readings)
        speed_factor = min(1.0, min_obs_dist / 1.5)
        turn_factor = max(0.2, np.cos(heading_err))
        v = self.v_max * speed_factor * turn_factor
        
        if dist_to_goal < 0.5:
            v = min(v, dist_to_goal * 0.5)
            
        return v, w

    def step(self, v, w):
        """Updates robot position based on kinematics."""
        self.heading += w * self.dt
        self.heading = np.arctan2(np.sin(self.heading), np.cos(self.heading))
        self.pos[0] += v * np.cos(self.heading) * self.dt
        self.pos[1] += v * np.sin(self.heading) * self.dt
        
        self.path_x.append(self.pos[0])
        self.path_y.append(self.pos[1])


def run_obstacle_detection_simulation():
    """Main simulation runner and visualization."""
    print("=" * 60)
    print("      PART B - TASK 1: OBSTACLE DETECTION ROBOT SIMULATION    ")
    print("=" * 60)
    
    # Environment Setup
    obstacles = [
        Obstacle('circle', (6.0, 6.0, 2.0)),
        Obstacle('circle', (14.0, 14.0, 2.2)),
        Obstacle('rect', (9.0, 3.0, 2.5, 6.0)),
        Obstacle('rect', (3.0, 12.0, 6.0, 2.0)),
        Obstacle('circle', (12.0, 8.0, 1.5)),
        Obstacle('circle', (6.0, 16.0, 1.8)),
    ]
    
    robot = ObstacleDetectionRobot(start_pos=(2.0, 2.0), goal_pos=(18.0, 18.0))
    
    max_steps = 600
    reached_goal = False
    
    print(f"[*] Starting position : {robot.pos}")
    print(f"[*] Target Goal       : {robot.goal}")
    print(f"[*] Total Obstacles   : {len(obstacles)}")
    print(f"[*] LIDAR Sensors     : {robot.num_rays} Rays (360 deg field)")
    print("[*] Running simulation step loop...")
    
    for step_i in range(max_steps):
        readings = robot.scan_environment(obstacles)
        v, w = robot.compute_apf_velocity(readings, obstacles)
        robot.step(v, w)
        
        dist_to_goal = np.linalg.norm(robot.goal - robot.pos)
        if dist_to_goal < 0.4:
            reached_goal = True
            print(f"[+] Target goal reached at step {step_i}! Distance: {dist_to_goal:.3f} m")
            break

    # Generate Visualization Figure
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_aspect('equal')
    ax.set_xlim(0, 20)
    ax.set_ylim(0, 20)
    ax.set_title("Part B.1: Autonomous Robot Obstacle Detection & Navigation", fontsize=14, fontweight='bold')
    ax.set_xlabel("X Position (meters)", fontsize=12)
    ax.set_ylabel("Y Position (meters)", fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.6)
    
    # Draw Obstacles
    for obs in obstacles:
        if obs.obs_type == 'circle':
            cx, cy, r = obs.params
            circle = Circle((cx, cy), r, color='#d9534f', alpha=0.7, label='Obstacle' if obs == obstacles[0] else "")
            ax.add_patch(circle)
        elif obs.obs_type == 'rect':
            rx, ry, w, h = obs.params
            rect = Rectangle((rx, ry), w, h, color='#d9534f', alpha=0.7)
            ax.add_patch(rect)
            
    # Draw Robot Trajectory
    ax.plot(robot.path_x, robot.path_y, 'b-', linewidth=2.5, label='Robot Trajectory')
    ax.plot(robot.path_x[0], robot.path_y[0], 'go', markersize=10, label='Start Point')
    ax.plot(robot.goal[0], robot.goal[1], 'r*', markersize=16, label='Goal Destination')
    
    # Draw Robot Body at final position
    robot_circle = Circle((robot.pos[0], robot.pos[1]), robot.radius, color='#0275d8', zorder=5, label='Robot Body')
    ax.add_patch(robot_circle)
    
    # Heading line
    hx = robot.pos[0] + robot.radius * 1.5 * np.cos(robot.heading)
    hy = robot.pos[1] + robot.radius * 1.5 * np.sin(robot.heading)
    ax.plot([robot.pos[0], hx], [robot.pos[1], hy], 'yellow', linewidth=3, zorder=6)
    
    # Draw sample LIDAR beams from final scan
    for hit_pt, angle, dist in robot.scan_hits:
        if hit_pt is not None:
            # Beam hit obstacle -> Red
            ax.plot([robot.pos[0], hit_pt[0]], [robot.pos[1], hit_pt[1]], 'r--', alpha=0.4, linewidth=0.8)
            ax.plot(hit_pt[0], hit_pt[1], 'ro', markersize=3, alpha=0.6)
        else:
            # Beam clear -> Green
            end_x = robot.pos[0] + robot.max_range * np.cos(angle)
            end_y = robot.pos[1] + robot.max_range * np.sin(angle)
            ax.plot([robot.pos[0], end_x], [robot.pos[1], end_y], 'g--', alpha=0.2, linewidth=0.5)

    ax.legend(loc='upper left', frameon=True, shadow=True)
    
    # Annotate stats
    info_text = f"Status: {'Goal Reached' if reached_goal else 'In Progress'}\nSteps: {len(robot.path_x)}\nPath Length: {np.sum(np.hypot(np.diff(robot.path_x), np.diff(robot.path_y))):.2f} m"
    ax.text(0.02, 0.02, info_text, transform=ax.transAxes, fontsize=11,
            bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.9, edgecolor='black'))
    
    output_img = os.path.join(os.path.dirname(__file__), "part_b_1_obstacle_detection_result.png")
    plt.tight_layout()
    plt.savefig(output_img, dpi=300)
    print(f"[+] Saved visualization image to: {output_img}")
    plt.close()
    
    print("=" * 60)
    print("Part B - Task 1 Simulation Completed Successfully!\n")

if __name__ == "__main__":
    run_obstacle_detection_simulation()
