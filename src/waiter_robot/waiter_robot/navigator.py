from nav2_simple_commander.robot_navigator import BasicNavigator
from geometry_msgs.msg import PoseStamped
import rclpy


class Navigator:

    def __init__(self):
        self.navigator = BasicNavigator()

    def go_to(self, x, y):
        goal = PoseStamped()
        goal.header.frame_id = 'map'
        goal.header.stamp = self.navigator.get_clock().now().to_msg()

        goal.pose.position.x = x
        goal.pose.position.y = y
        goal.pose.orientation.w = 1.0

        self.navigator.goToPose(goal)

        while not self.navigator.isTaskComplete():
            pass

        print(f"Reached ({x}, {y})")
