import rclpy
from rclpy.node import Node
from robot_safety_interfaces.msg import SensorData
from std_msgs.msg import String

from rich.console import Console
from rich.table import Table

class TerminalDashboard(Node):
    def __init__(self):
        super().__init__('terminal_dashboard')
        self.console = Console()
        
        self.battery = 100.0
        self.temp = 30.0
        self.cpu = 50.0
        self.status = "NORMAL"

  
        self.sub_sensor = self.create_subscription(SensorData, 'sensor_data', self.sensor_cb, 10)
        self.sub_status = self.create_subscription(String, 'robot_status', self.status_cb, 10)
        
        self.timer = self.create_timer(0.5, self.draw_screen)

    def sensor_cb(self, msg):
    
        self.battery = msg.battery_level
        self.temp = msg.motor_temp
        self.cpu = msg.cpu_load

    def status_cb(self, msg):
        self.status = msg.data

    def draw_screen(self):
        
        table = Table(title=" ROBOT SAFETY DASHBOARD ", show_header=True, header_style="bold magenta")
        table.add_column("Mesure", style="cyan", no_wrap=True)
        table.add_column("Valeur", justify="right")
        table.add_column("État", justify="center")

    
        bat_style = "green" if self.battery > 30 else "bold red"
        temp_style = "green" if self.temp < 60 else "bold red"
        status_style = "green" if self.status == "NORMAL" else "bold red"

  
        table.add_row(" Batterie", f"{self.battery:.1f} %", f"[{bat_style}]{self.battery:.0f}%[/{bat_style}]")
        table.add_row(" Température", f"{self.temp:.1f} °C", f"[{temp_style}]{self.temp:.0f}°C[/{temp_style}]")
        table.add_row(" CPU", f"{self.cpu:.1f} %", f"{self.cpu:.0f}%")
        table.add_row(" Status", self.status, f"[{status_style}]{self.status}[/{status_style}]")

       
        self.console.clear()
        self.console.print(table)

def main(args=None):
    rclpy.init(args=args)
    node = TerminalDashboard()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
