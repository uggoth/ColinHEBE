module_name = 'main_escape_route_v02.py'
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
CommandStream = SourceFileLoader('CommandStream', '/home/pi/ColinPiClasses/' + data_values['CommandStream'] + '.py').load_module()
import time
import pigpio
gpio = pigpio.pi()
import sys
handshake = CommandStream.Handshake(4, gpio)
from vl53l5cx.vl53l5cx import VL53L5CX
pico_id = 'PICOA'
my_pico = CommandStream.Pico(pico_id, gpio, handshake)
pwren = 17
gpio.set_mode(pwren, pigpio.OUTPUT)
gpio.write(pwren,1)
blue_button = 16
gpio.set_mode(blue_button, pigpio.INPUT)
gpio.set_pull_up_down(blue_button, pigpio.PUD_UP)
driver = VL53L5CX()
my_ultrasonics = ThisPi.Ultrasonics(gpio)
my_front_ultrasonic = my_ultrasonics.front_ultrasonic.instance

alive = driver.is_alive()
if not alive:
    raise IOError("VL53L5CX Device is not alive")

print("Initialising...")
t = time.time()
driver.init()
for i in range(9):
    mmus = my_front_ultrasonic.read_mms()
    time.sleep(0.2)
print(f"Initialised ({time.time() - t:.1f}s)")
print ('Now waiting for blue button')
no_loops = 1000
for i in range(no_loops):
    time.sleep(0.01)
    if gpio.read(blue_button) == 0:
        break
if i >= no_loops:
    print ('Blue button not pressed. Exiting')
    sys.exit(1)
print ('Blue button pressed. Starting ...')
driver.set_resolution(4*4)
driver.set_ranging_frequency_hz(20)
# Ranging:
driver.start_ranging()

####### DRIV parameters are 4 digit integers for throttle and steering
####### e.g DRIV00500010 is 50% throttle, and 10% right

no_loops = 50
no_zones = 16
interval = 300  #  milliseconds
for i in range(no_loops):
    serial_no = '{:04}'.format(i)
    time.sleep(interval / 1000.0)
    if driver.check_data_ready():
        ranging_data = driver.get_ranging_data()
        st15 = ranging_data.target_status[driver.nb_target_per_zone * 15]
        st11 = ranging_data.target_status[driver.nb_target_per_zone * 11]
        st07 = ranging_data.target_status[driver.nb_target_per_zone * 7]
        st03 = ranging_data.target_status[driver.nb_target_per_zone * 3]
        if not ((st15 == 5) and (st15 == 5) and (st15 == 5) and (st15 == 5)):
            continue
        mm15 = int(ranging_data.distance_mm[driver.nb_target_per_zone * 15])
        mm11 = int(ranging_data.distance_mm[driver.nb_target_per_zone * 11])
        mm07 = int(ranging_data.distance_mm[driver.nb_target_per_zone * 7])
        mm03 = int(ranging_data.distance_mm[driver.nb_target_per_zone * 3])
        mmus = my_front_ultrasonic.read_mms()
        print ('{:4}  {:4}  {:4}  {:4}  {:4}  '.format(mm15,mm11,mm07,mm03,mmus))
        
        avg_offset = (mm15 + mm11 + mm07 + mm03) / 4
        if avg_offset < 150:
            offset = 'TOO_CLOSE'
        elif avg_offset > 200:
            offset = 'TOO_FAR'
        else:
            offset = 'DISTANCE_OK'
            
        avg_angle = (mm15 + mm11) / (mm07 + mm03)
        if avg_angle < 0.95:
            angle = 'OPENING'
        elif avg_angle > 1.05:
            angle = 'CLOSING'
        else:
            angle = 'ANGLE_OK'
            
        if mmus < 150:
            front = 'HITTING'
        elif mmus > 220:
            front = 'CLEAR_AHEAD'
        else:
            front = 'APPROACHING'
            
        if front == 'CLEAR_AHEAD':
            throttle = 40
        elif front == 'APPROACHING':
            throttle = 20
        else:
            throttle = 0

        steering_info = offset + ' ' + angle
        steering_calc = {
            'TOO_CLOSE OPENING':0,
            'TOO_CLOSE CLOSING':40,
            'TOO_CLOSE ANGLE_OK':10,
            'TOO_FAR OPENING':-30,
            'TOO_FAR CLOSING':0,
            'TOO_FAR ANGLE_OK':20,
            'DISTANCE_OK OPENING':-10,
            'DISTANCE_OK CLOSING':15,
            'DISTANCE_OK ANGLE_OK':0
            }

        steering = steering_calc[steering_info]

        command = 'DRIV{:04}{:04}'.format(throttle, steering)
        print (offset, angle, front, command)
        print (my_pico.do_command(serial_no, command), '\n')
            
            
    time.sleep(0.005)
my_pico.do_command(serial_no, 'STOP')
print (module_name, 'finished')
