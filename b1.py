import matplotlib.pyplot as plt
import numpy as np


class ObstacleDetectionRobot:

  def __init__(self, start_pos=(0, 0), sensor_range=2.5, num_sensors=7):
    self.pos = np.array(start_pos, dtype=float)
    self.heading = 0.0  # Radians
    self.sensor_range = sensor_range
    self.num_sensors = num_sensors
    # Sensor field of view: -60 degrees to +60 degrees
    self.sensor_angles = np.linspace(-np.pi / 3, np.pi / 3, num_sensors)
    self.path = [self.pos.copy()]

  def detect_obstacles(self, obstacles):
    """Simulates ray-casting sensor readings against circular obstacles."""
    distances = np.full(self.num_sensors, self.sensor_range)

    for i, angle in enumerate(self.sensor_angles):
      ray_angle = self.heading + angle
      ray_dir = np.array([np.cos(ray_angle), np.sin(ray_angle)])

      for obs_pos, obs_radius in obstacles:
        d = np.array(obs_pos) - self.pos
        proj = np.dot(d, ray_dir)

        if proj > 0:  # Obstacle is in front of ray
          perp_dist = np.linalg.norm(d - proj * ray_dir)
          if perp_dist < obs_radius:
            hit_dist = proj - np.sqrt(obs_radius**2 - perp_dist**2)
            if 0 < hit_dist < distances[i]:
              distances[i] = hit_dist
    return distances

  def update(self, goal, obstacles, speed=0.15):
    """Updates robot heading and position based on sensor feedback."""
    sensor_dists = self.detect_obstacles(obstacles)
    min_dist = np.min(sensor_dists)
    front_idx = self.num_sensors // 2

    # Obstacle avoidance mode
    if min_dist < 1.2:
      left_clearance = np.mean(sensor_dists[:front_idx])
      right_clearance = np.mean(sensor_dists[front_idx + 1 :])

      # Turn away from obstacle toward open space
      if left_clearance > right_clearance:
        self.heading += 0.25  # Turn left
      else:
        self.heading -= 0.25  # Turn right
    else:
      # Navigation mode: head toward target
      goal_vector = np.array(goal) - self.pos
      target_angle = np.arctan2(goal_vector[1], goal_vector[0])
      angle_diff = (target_angle - self.heading + np.pi) % (
          2 * np.pi
      ) - np.pi
      self.heading += np.clip(angle_diff, -0.2, 0.2)

    # Step forward
    self.pos += speed * np.array([np.cos(self.heading), np.sin(self.heading)])
    self.path.append(self.pos.copy())


# --- Simulation Run ---
np.random.seed(42)
start_point = (0.0, 0.0)
target_point = (10.0, 10.0)

# Define Obstacles: [(x, y), radius]
obstacles = [
    ((2.5, 2.0), 1.0),
    ((5.0, 5.5), 1.3),
    ((7.5, 6.0), 1.0),
    ((4.0, 8.0), 0.9),
    ((8.0, 2.5), 1.2),
]

robot = ObstacleDetectionRobot(start_pos=start_point)

# Execute navigation loop
for _ in range(120):
  robot.update(target_point, obstacles)
  if np.linalg.norm(robot.pos - np.array(target_point)) < 0.5:
    print("Goal reached successfully!")
    break

# --- Plotting Simulation ---
fig, ax = plt.subplots(figsize=(8, 8))

# Draw Obstacles
for obs_pos, obs_radius in obstacles:
  circle = plt.Circle(
      obs_pos,
      obs_radius,
      color='crimson',
      alpha=0.6,
      label='Obstacle' if obs_pos == obstacles[0][0] else '',
  )
  ax.add_patch(circle)

# Draw Robot Trajectory
path_arr = np.array(robot.path)
ax.plot(
    path_arr[:, 0],
    path_arr[:, 1],
    'b--',
    linewidth=2,
    label='Robot Trajectory',
)
ax.scatter(*start_point, color='green', s=120, zorder=5, label='Start')
ax.scatter(
    *target_point, color='gold', marker='*', s=200, zorder=5, label='Goal'
)

# Draw Robot Sensor Rays at final step
final_sensor_dists = robot.detect_obstacles(obstacles)
for angle, dist in zip(robot.sensor_angles, final_sensor_dists):
  ray_angle = robot.heading + angle
  end_x = robot.pos[0] + dist * np.cos(ray_angle)
  end_y = robot.pos[1] + dist * np.sin(ray_angle)
  ax.plot(
      [robot.pos[0], end_x],
      [robot.pos[1], end_y],
      color='orange',
      linestyle=':',
      alpha=0.7,
  )

ax.set_title('Obstacle Detection & Avoidance Simulation')
ax.set_xlabel('X Position (m)')
ax.set_ylabel('Y Position (m)')
ax.legend(loc='upper left')
ax.set_aspect('equal')
plt.grid(True)
plt.show()