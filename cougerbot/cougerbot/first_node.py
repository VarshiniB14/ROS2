import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from builtin_interfaces.msg import Duration

class ManipulatorController(Node):
    def __init__(self):
        super().__init__('manipulator_controller')
        self.publisher = self.create_publisher(JointTrajectory, '/joint_trajectory_controller/joint_trajectory', 10)
        self.timer = self.create_timer(3.0, self.move_manipulator)
        self.current_position_index = 0

        self.positions = []
        
        R = [
            [0.0, -0.11, 1.4, 0.0],
            [3.14, -0.11, 1.4, 0.0]
        ]
        
        G = [
            [1.0, 0.4, 0.0, 0.0],
            [2.20, 0.4, 0.0, 0.0]
        ]
        
        B = [
            [-1.0, 0.25, 0.3, 0.0],
            [-2.15, 0.25, 0.3, 0.0]
        ]

        print("Enter a colour in R G B:")
        alphabet = input()

        if alphabet == 'R':
            self.positions = R
        elif alphabet == 'G':
            self.positions = G
        elif alphabet == 'B':
            self.positions = B
        else:
            self.positions = []
            print("Invalid alphabet entered!")

    def move_manipulator(self):
        if self.current_position_index >= len(self.positions):
            self.get_logger().info("Manipulator reached the final position.")
            return

        position = self.positions[self.current_position_index]
        self.get_logger().info(f"Moving manipulator to position: {position}")

        trajectory = JointTrajectory()
        trajectory.joint_names = ['hip', 'shoulder', 'elbow', 'wrist']

        point = JointTrajectoryPoint()
        point.positions = position
        point.time_from_start = Duration(sec=2)  # Set seconds

        trajectory.points.append(point)
        self.publisher.publish(trajectory)

        self.current_position_index += 1

def main(args=None):
    rclpy.init(args=args)
    manipulator_controller = ManipulatorController()
    rclpy.spin(manipulator_controller)
    manipulator_controller.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

