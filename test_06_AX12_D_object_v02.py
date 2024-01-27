module_name = 'test_06_AX12_D_object_v02.py'

print (module_name, 'starting')

from importlib.machinery import SourceFileLoader
data_module = SourceFileLoader('Colin', '/home/pi/ColinThisPi/ColinData.py').load_module()
data_object = data_module.ColinData()
data_values = data_object.params
ThisPiVersion = data_values['ThisPi']
ThisPi = SourceFileLoader('ThisPi', '/home/pi/ColinThisPi/' + ThisPiVersion + '.py').load_module()

zombie_arm = ThisPi.ZombieArm()

wrist_servo = zombie_arm.wrist_servo

wrist_servo.move_to_and_wait(-100)
wrist_servo.move_to_and_wait(33, 100)
wrist_servo.move_to_and_wait(53, 10)
wrist_servo.move_to_and_wait(100)
wrist_servo.move_to_and_wait(-100, 90)
wrist_servo.move_to_and_wait(0, 90)

zombie_arm.close()
