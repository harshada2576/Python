import numpy as np
import matplotlib.pyplot as plt


class SpaceRoboticArm3D:

  def __init__(self, link_lengths, base_position=(0, 0, 0)):
    """Initialize a 3D Robotic Arm with specified link lengths."""
    self.link_lengths = np.array(link_lengths, dtype=float)
    self.num_joints = len(link_lengths) + 1
    self.base_position = np.array(base_position, dtype=float)

    # Initialize joint positions vertically along Z-axis
    self.joints = np.zeros((self.num_joints, 3))
    self.joints[0] = self.base_position
    for i in range(len(link_lengths)):
      self.joints[i + 1] = self.joints[i] + np.array(
          [0, 0, self.link_lengths[i]]
      )

  def reach_target(self, target, max_iter=100, tolerance=1e-3):
    """Solves Inverse Kinematics using 3D FABRIK algorithm."""
    target = np.array(target, dtype=float)
    total_reach = np.sum(self.link_lengths)
    dist_to_target = np.linalg.norm(target - self.joints[0])

    # Case 1: Target is out of reach
    if dist_to_target > total_reach:
      print("[Warning] Target outside workspace reach. Extending fully.")
      for i in range(self.num_joints - 1):
        r = np.linalg.norm(target - self.joints[i])
        lambda_factor = self.link_lengths[i] / r
        self.joints[i + 1] = (1 - lambda_factor) * self.joints[
            i
        ] + lambda_factor * target
      return False, np.linalg.norm(self.joints[-1] - target)

    # Case 2: Target within reach, perform iterative FABRIK
    base_fixed = np.copy(self.joints[0])
    dist = np.linalg.norm(self.joints[-1] - target)
    iteration = 0

    while dist > tolerance and iteration < max_iter:
      # Forward Phase: Start from end-effector set to target
      self.joints[-1] = target
      for i in range(self.num_joints - 2, -1, -1):
        r = np.linalg.norm(self.joints[i + 1] - self.joints[i])
        lambda_factor = self.link_lengths[i] / (r + 1e-8)
        self.joints[i] = (1 - lambda_factor) * self.joints[
            i + 1
        ] + lambda_factor * self.joints[i]

      # Backward Phase: Reset base and adjust forward
      self.joints[0] = base_fixed
      for i in range(self.num_joints - 1):
        r = np.linalg.norm(self.joints[i + 1] - self.joints[i])
        lambda_factor = self.link_lengths[i] / (r + 1e-8)
        self.joints[i + 1] = (1 - lambda_factor) * self.joints[
            i
        ] + lambda_factor * self.joints[i + 1]

      dist = np.linalg.norm(self.joints[-1] - target)
      iteration += 1

    return True, dist

  def visualize(self, target, title='Space Station 3D Manipulator'):
    """Plot the 3D position of the arm and target in space."""
    fig = plt.figure(figsize=(9, 7))
    ax = fig.add_subplot(111, projection='3d')

    # Coordinates extraction
    x = self.joints[:, 0]
    y = self.joints[:, 1]
    z = self.joints[:, 2]

    # Plot arm segments & joints
    ax.plot(
        x,
        y,
        z,
        '-o',
        color='navy',
        linewidth=4,
        markersize=8,
        label='Robotic Arm Links',
    )

    # Plot base, end-effector, and target position
    ax.scatter(
        *self.joints[0],
        color='black',
        s=120,
        zorder=5,
        label='Space Station Base',
    )
    ax.scatter(
        *self.joints[-1],
        color='limegreen',
        s=100,
        zorder=5,
        label='End-Effector Position',
    )
    ax.scatter(
        *target,
        color='crimson',
        s=120,
        marker='X',
        zorder=5,
        label='Target Payload Position',
    )

    ax.set_xlabel('X Axis (meters)')
    ax.set_ylabel('Y Axis (meters)')
    ax.set_zlabel('Z Axis (meters)')
    ax.set_title(title)
    ax.legend(loc='upper left')
    plt.show()


# Example Execution
if __name__ == '__main__':
  # Define 4 link segments for a flexible space arm (lengths in meters)
  segment_lengths = [2.5, 2.0, 1.5, 1.0]
  space_arm = SpaceRoboticArm3D(link_lengths=segment_lengths)

  # Target coordinate in 3D space
  target_coordinate = [3.0, 2.5, 1.8]

  # Solve IK
  success, final_error = space_arm.reach_target(target_coordinate)

  print(f"Status: {'SUCCESS' if success else 'FAILED'}")
  print(f'Final End-Effector Error: {final_error:.6f} meters')
  print('\nComputed Joint Coordinates:')
  for idx, joint in enumerate(space_arm.joints):
    print(f' Joint {idx}: [{joint[0]:.3f}, {joint[1]:.3f}, {joint[2]:.3f}]')

  # Generate 3D plot
  space_arm.visualize(target_coordinate)