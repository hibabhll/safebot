import rclpy
from rclpy.node import Node
from robot_safety_interfaces.msg import SensorData
from std_msgs.msg import String
import csv
import os
from datetime import datetime


class DataLogger(Node):
    def __init__(self):
        super().__init__('data_logger')
        self.last_status = 'NORMAL'

        # Dossier mte3 l'logs f dar (home)
        self.log_dir = os.path.expanduser('~/robot_logs')
        os.makedirs(self.log_dir, exist_ok=True)

        # Ism l'fichier b l'wa9t (kol session = fichier jdid)
        filename = datetime.now().strftime('session_%Y%m%d_%H%M%S.csv')
        self.filepath = os.path.join(self.log_dir, filename)

        # N7ellou l'fichier w nktebou l'titre mte3 l'colonnes
        self.file = open(self.filepath, 'w', newline='')
        self.writer = csv.writer(self.file)
        self.writer.writerow(['timestamp', 'battery', 'temp', 'cpu', 'status'])

        self.sub_sensor = self.create_subscription(
            SensorData, 'sensor_data', self.sensor_cb, 10)
        self.sub_status = self.create_subscription(
            String, 'robot_status', self.status_cb, 10)
        self.get_logger().info(f'Data Logger demarre! Fichier: {self.filepath}')

    def sensor_cb(self, msg):
        # Kol message = sطر jdid f l'CSV
        self.writer.writerow([
            msg.timestamp,
            f'{msg.battery_level:.1f}',
            f'{msg.motor_temp:.1f}',
            f'{msg.cpu_load:.1f}',
            self.last_status
        ])
        self.file.flush()   # ⚡ Nktebou 3la l'disque FAWRAN (ken l'PC ytafi, ma ndhay3ouch l'données!)

    def status_cb(self, msg):
        self.last_status = msg.data


def main(args=None):
    rclpy.init(args=args)
    node = DataLogger()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.file.close()   # Nghal9ou l'fichier b adab 9bal ma nemchiw
        rclpy.shutdown()


if __name__ == '__main__':
    main()
