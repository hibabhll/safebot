import rclpy
from rclpy.node import Node
from robot_safety_interfaces.msg import SensorData
from std_msgs.msg import String

class HealthMonitor(Node):
    def __init__(self):
        super().__init__('health_monitor')
        
        # 1. L'ODHNIN W L'FOMM (kima lbere7)
        self.subscription = self.create_subscription(
            SensorData, 'sensor_data', self.listener_callback, 10)
        self.publisher_ = self.create_publisher(String, 'robot_status', 10)

        # 2. 💎 L'PARAMETERS: N3arfou l ROS2 enna 3andna 4 paramètres, w l'défaut mte3hom hakka:
        self.declare_parameter('temp_warn', 60.0)
        self.declare_parameter('temp_crit', 75.0)
        self.declare_parameter('batt_warn', 30.0)
        self.declare_parameter('batt_crit', 15.0)

        self.get_logger().info('Health Monitor demarre (b Parameters)!')

    def listener_callback(self, msg):
        # 3. N9RAW L'PARAMÈTRES (kol marra yji message, bash ken badlnahom LIVE, ya9rahom dghar)
        temp_warn = self.get_parameter('temp_warn').value
        temp_crit = self.get_parameter('temp_crit').value
        batt_warn = self.get_parameter('batt_warn').value
        batt_crit = self.get_parameter('batt_crit').value

        # 4. L'MACHINE À ÉTATS (tawa b l'variables, machi b l'ar9am msamra!)
        if msg.motor_temp >= temp_crit or msg.battery_level <= batt_crit:
            status = 'CRITICAL'
        elif msg.motor_temp >= temp_warn or msg.battery_level <= batt_warn:
            status = 'WARNING'
        else:
            status = 'NORMAL'

        out = String()
        out.data = status
        self.publisher_.publish(out)
        
        self.get_logger().info(
            f'Etat: {status} | T:{msg.motor_temp:.1f}C (Crit:{temp_crit}) | B:{msg.battery_level:.1f}% (Crit:{batt_crit})')

def main(args=None):
    rclpy.init(args=args)
    node = HealthMonitor()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
