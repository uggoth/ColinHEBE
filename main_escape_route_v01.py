module_name = 'main_escape_route_v01.py'
print (module_name, 'starting')
print ('expects main_autonomous to be running on the Pico')

from importlib.machinery import SourceFileLoader
data_module = SourceFileLoader('Colin', '/home/pi/ColinThisPi/ColinData.py').load_module()
data_object = data_module.ColinData()
data_values = data_object.params
ColObjectsVersion = data_values['ColObjects']
col_objects_name = '/home/pi/ColinPiClasses/' + ColObjectsVersion + '.py'
ColObjects = SourceFileLoader('ColObjects', col_objects_name).load_module()
ThisPiVersion = data_values['ThisPi']
pi_version = '/home/pi/ColinThisPi/' + ThisPiVersion + '.py'
ThisPi = SourceFileLoader('ThisPi', pi_version).load_module()
CommandStream = SourceFileLoader('CommandStream', '/home/pi/ColinPiClasses/' +
                                 data_values['CommandStream'] + '.py').load_module()
import time
import pigpio
gpio = pigpio.pi()
handshake = CommandStream.Handshake(4, gpio)
pico_id = 'PICOA'
my_pico = CommandStream.Pico(pico_id, gpio, handshake)

####### DRIV parameters are 4 digit integers for throttle and steering
####### e.g DRIV00500010 is 50% throttle, and 10% right

i = 0
commands = ['DRIV  30  20',
            'DRIV  40 -10',
            'DRIV -30   0',
            'STOP',
            'DRIV  30 -10',
            'DRIV -30   0',
            'EXIT']
for command in commands:
    time.sleep(1)
    i += 1
    serial_no = '{:04}'.format(i)
    my_pico.do_command(serial_no, command)

#print ('Before Close\n',ColObjects.ColObj.str_allocated())
ColObjects.ColObj.close_all()
#print ('After Close\n',ColObjects.ColObj.str_allocated())
print (module_name, 'finished')
