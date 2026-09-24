import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class SafetyController(Node):
    def __init__(self):
        super().__init__('safety_controller')
        self.subscription = self.create_subscription(
            String, 'robot_status', self.listener_callback, 10)
        self.last_status = ''
        self.get_logger().info('Safety Controller demarre!')

    def listener_callback(self, msg):
        if msg.data == self.last_status:
            return
        self.last_status = msg.data

        if msg.data == 'CRITICAL':
            self.get_logger().error('SAFE MODE ACTIVATED! Robot w9af: batterie/temp critiques!')
        elif msg.data == 'WARNING':
            self.get_logger().warn('WARNING: robot bda yn9os l-vitesse...')
        else:
            self.get_logger().info('NORMAL: robot ykhedem b ri7et balek.')


def main(args=None):
    rclpy.init(args=args)
    node = SafetyController()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
