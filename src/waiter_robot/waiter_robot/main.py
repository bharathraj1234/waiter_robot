import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import time

from waiter_robot.navigator import Navigator


class FSMNode(Node):

    def __init__(self):
        super().__init__('fsm_node')

        # Subscribers
        self.create_subscription(String, '/order', self.order_callback, 10)
        self.create_subscription(String, '/confirm', self.confirm_callback, 10)
        self.create_subscription(String, '/cancel', self.cancel_callback, 10)

        self.navigator = Navigator()

        # FSM data
        self.orders = []
        self.current_order = None
        self.confirmed = None
        self.cancelled = False

        self.has_food = False
        self.skipped_any = False
        self.moving_to = None

        self.state = "IDLE"

        # positions
        self.home = (0.0, -4.0)
        self.kitchen = (3.0, -3.5)
        self.tables = {
            "table1": (-3.4, 2.0),
            "table2": (-1.7, 2.0),
            "table3": (0.4, 2.0),
            "table4": (3.0, 2.0),
            "table5": (4.4, 2.0),
        }

        self.timer = self.create_timer(1.0, self.run)
        self.get_logger().info("🤖 FSM Started and waiting for orders...")

    # ---------------- CALLBACKS ---------------- #

    def order_callback(self, msg):
        self.orders.append(msg.data)
        self.get_logger().info(f"📥 Order received → {msg.data}")

    def confirm_callback(self, msg):
        self.confirmed = msg.data.lower()
        self.get_logger().info(f"📩 Confirm message → {self.confirmed}")

    def cancel_callback(self, msg):
        self.cancelled = True
        self.get_logger().warn("❌ Cancel signal received!")

    # ---------------- FSM ---------------- #

    def run(self):

        # 🔥 GLOBAL CANCEL HANDLER
        if self.cancelled:
            self.get_logger().warn("🚨 Handling cancel...")

            if self.moving_to == "KITCHEN":
                self.get_logger().info("➡️ Cancel during kitchen travel → HOME")
                self.state = "RETURN_HOME"

            elif self.moving_to == "TABLE":
                self.get_logger().info("➡️ Cancel during table travel → KITCHEN → HOME")
                self.state = "RETURN_KITCHEN"

            else:
                self.get_logger().info("➡️ Cancel → HOME")
                self.state = "RETURN_HOME"

            self.cancelled = False
            return

        # ---------------- IDLE ---------------- #
        if self.state == "IDLE":

            self.get_logger().info("🟡 Waiting for orders...")

            if self.orders:
                self.get_logger().info("🚀 Order received → Going to kitchen")

                self.moving_to = "KITCHEN"
                self.navigator.go_to(*self.kitchen)

                self.state = "WAIT_KITCHEN"
                self.confirmed = None
                self.start_time = time.time()

        # ---------------- WAIT KITCHEN ---------------- #
        elif self.state == "WAIT_KITCHEN":

            self.get_logger().info("🍳 Waiting for kitchen confirmation (yes/no)...")

            if self.confirmed == "yes":
                self.get_logger().info("✅ Food collected from kitchen")
                self.has_food = True
                self.skipped_any = False
                self.state = "NEXT_TABLE"

            elif self.confirmed == "no":
                self.get_logger().warn("❌ Kitchen rejected order → HOME")
                self.orders.clear()
                self.state = "RETURN_HOME"

            elif time.time() - self.start_time > 10:
                self.get_logger().warn("⌛ Kitchen timeout → HOME")
                self.orders.clear()
                self.state = "RETURN_HOME"

        # ---------------- NEXT TABLE ---------------- #
        elif self.state == "NEXT_TABLE":

            if not self.orders:
                self.get_logger().info("✅ Finished all tables")

                if self.skipped_any:
                    self.get_logger().info("⚠️ Some tables skipped → Returning kitchen first")
                    self.state = "RETURN_KITCHEN"
                else:
                    self.get_logger().info("🎉 All delivered → Going HOME")
                    self.state = "RETURN_HOME"
                return

            self.current_order = self.orders.pop(0)

            if self.current_order not in self.tables:
                self.get_logger().warn(f"⚠️ Unknown table {self.current_order}")
                return

            self.get_logger().info(f"🍽️ Heading to {self.current_order}")

            self.moving_to = "TABLE"
            self.navigator.go_to(*self.tables[self.current_order])

            self.confirmed = None
            self.start_time = time.time()
            self.state = "WAIT_TABLE"

        # ---------------- WAIT TABLE ---------------- #
        elif self.state == "WAIT_TABLE":

            self.get_logger().info(f"⏳ Waiting for confirmation at {self.current_order}...")

            if self.confirmed == "yes":
                self.get_logger().info(f"✅ Delivered → {self.current_order}")
                self.state = "NEXT_TABLE"

            elif time.time() - self.start_time > 8:
                self.get_logger().warn(f"⌛ No response at {self.current_order} → Skipping")
                self.skipped_any = True
                self.state = "NEXT_TABLE"

        # ---------------- RETURN KITCHEN ---------------- #
        elif self.state == "RETURN_KITCHEN":

            self.get_logger().info("🍳 Returning to kitchen (remaining food)")

            self.navigator.go_to(*self.kitchen)

            self.has_food = False
            self.state = "RETURN_HOME"

        # ---------------- RETURN HOME ---------------- #
        elif self.state == "RETURN_HOME":

            self.get_logger().info("🏠 Returning to HOME")

            self.navigator.go_to(*self.home)

            self.state = "IDLE"


def main(args=None):
    rclpy.init(args=args)
    node = FSMNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
