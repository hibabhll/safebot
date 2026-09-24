import rclpy
from rclpy.node import Node
from robot_safety_interfaces.msg import SensorData
import random
import time


class SensorSimulator(Node):
    def __init__(self):
        super().__init__('sensor_simulator')

        self.publisher_ = self.create_publisher(SensorData, 'sensor_data', 10)

        self.timer_ = self.create_timer(1.0, self.publish_data)

        self.battery = 100.0
        self.temp = 30.0

        self.get_logger().info('Sensor Simulator demarre!')

    def publish_data(self):
        self.battery = max(0.0, self.battery - random.uniform(0.1, 0.5))
        self.temp = min(85.0, self.temp + random.uniform(0.05, 0.4))
        cpu = random.uniform(40.0, 80.0)

        msg = SensorData()
        msg.battery_level = self.battery
        msg.motor_temp = self.temp
        msg.cpu_load = cpu
        msg.timestamp = time.strftime('%H:%M:%S')

        self.publisher_.publish(msg)
        self.get_logger().info(
            f'Publie | B:{msg.battery_level:.1f}% | T:{msg.motor_temp:.1f}C | CPU:{msg.cpu_load:.1f}%')


def main(args=None):
    rclpy.init(args=args)
    node = SensorSimulator()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
