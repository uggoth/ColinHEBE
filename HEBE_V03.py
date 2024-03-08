module_name = 'BENJI_V02.py'
module_description = 'Objects for Raspberry Pi BENJI'
module_last_modified = '202401031240'

from importlib.machinery import SourceFileLoader
data_module = SourceFileLoader('Colin', '/home/pi/ColinThisPi/ColinData.py').load_module()
data_object = data_module.ColinData()
data_values = data_object.params
ColObjectsVersion = data_values['ColObjects']
ColObjects = SourceFileLoader('ColObjects', '/home/pi/ColinPiClasses/' + ColObjectsVersion + '.py').load_module()
GPIOVersion = data_values['GPIO']
GPIO = SourceFileLoader('GPIO', '/home/pi/ColinPiClasses/' + GPIOVersion + '.py').load_module()
CommandStreamVersion = data_values['CommandStream']
CommandStream = SourceFileLoader('CommandStream', '/home/pi/ColinPiClasses/' + CommandStreamVersion + '.py').load_module()
AX12ServoVersion = data_values['AX12Servo']
AX12Servo = SourceFileLoader('AX12Servo', '/home/pi/ColinPiClasses/' + AX12ServoVersion + '.py').load_module()
pico_name = data_values['PICO_NAME']

class ZombieArm(ColObjects.ColObj):
    def __init__(self):
        global data_values
        super().__init__('Zombie Arm','2 servo arm for Nerf gun')
        ax12_path = data_values['AX12_PATH']
        ax12_speed = data_values['AX12_SPEED']
        self.ax12_connection = AX12Servo.Connection(port=ax12_path, baudrate=ax12_speed)
        self.base_servo = AX12Servo.AX12Servo('Base Servo', self.ax12_connection, 20)
        self.wrist_servo = AX12Servo.AX12Servo('Wrist Servo', self.ax12_connection, 21)
        self.wrist_servo.clockwise_label = 'UP'
        self.wrist_servo.anticlockwise_label = 'DOWN'
        self.servo_list = [self.base_servo,self.wrist_servo]
    def close(self):
        self.base_servo.close()
        self.wrist_servo.close()
        super().close()

if __name__ == "__main__":
    print (module_name)
    print (module_description)
