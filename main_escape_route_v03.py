module_name = 'main_escape_route_v03.py'
print (module_name, 'starting')
print ('expects main_autonomous to be running on the Pico')

from importlib.machinery import SourceFileLoader
data_module = SourceFileLoader('Colin', '/home/pi/ColinHEBE/ColinData.py').load_module()
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
from datetime import datetime
now = datetime.now()
date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
my_pico.do_command('0000', 'LOGD'+date_time)
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
flash_loops = 10
flip_flop = False
for i in range(no_loops):
    time.sleep(0.01)
    if gpio.read(blue_button) == 0:
        break
    if i%flash_loops == 0:
        flip_flop = not flip_flop
        if flip_flop:
            my_pico.do_command('0000', 'RLC+')
        else:
            my_pico.do_command('0000', 'RLC-')
            
if i >= no_loops:
    print ('Blue button not pressed. Exiting')
    sys.exit(1)
print ('Blue button pressed. Starting ...')
driver.set_resolution(4*4)
driver.set_ranging_frequency_hz(40)
# Ranging:
driver.start_ranging()

def straighten_up():
    for i in range(9):
        time.sleep(0.05)
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
            print ('mm15:{:4}  mm11:{:4}  mm07:{:4}  mm03:{:4}'.format(mm15,mm11,mm07,mm03))
            left = (mm15+mm11)/2
            right = (mm07+mm03)/2
            diff = abs(left-right)
            if diff < 5:
                print ('Straight')
                break
            if left < right:
                command = 'TRNL0040'
            else:
                command = 'TRNR0040'
            my_pico.do_command('0000', command)

####### DRIV parameters are 4 digit integers for throttle and steering
####### e.g DRIV00500010 is 50% throttle, and 10% right

no_loops = 150
no_zones = 16
interval = 300  #  milliseconds
legs = ['TRNR 400','TRNR 400','STOP']
leg = 0
for i in range(no_loops):
    time.sleep(interval / 1000.0)
    serial_no = '{:04}'.format(i+1)
    mmus = my_front_ultrasonic.read_mms()
    if mmus < 190:
        print (mmus,'************ LEG', leg, legs[leg], '***********')
        my_pico.send_command_and_wait(serial_no, legs[leg])
        straighten_up()
        #mmus = my_front_ultrasonic.read_mms()
        #time.sleep(0.5)
        #mmus = my_front_ultrasonic.read_mms()
        #time.sleep(5)
        leg += 1
        if leg >= len(legs):
            break
        else:
            continue
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
        print ('mm15:{:4}  mm11:{:4}  mm07:{:4}  mm03:{:4}  mmus{:4}  '.format(mm15,mm11,mm07,mm03,mmus))

        if mm03 > 300:
            my_pico.do_command(serial_no, 'STOP')
            time.sleep(0.1)
            my_pico.do_command(serial_no, 'EXIT')
            break
        
        avg_offset = (mm15 + mm11 + mm07 + mm03) / 4
        if avg_offset < 140:
            offset = 'TOO_CLOSE'
        elif avg_offset > 180:
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
            
        steering_info = offset + ' ' + angle
        steering_calc = {
            'TOO_CLOSE OPENING':0,
            'TOO_CLOSE CLOSING':30,
            'TOO_CLOSE ANGLE_OK':10,
            'TOO_FAR OPENING':-40,
            'TOO_FAR CLOSING':0,
            'TOO_FAR ANGLE_OK':20,
            'DISTANCE_OK OPENING':-10,
            'DISTANCE_OK CLOSING':15,
            'DISTANCE_OK ANGLE_OK':0
            }

        steering = steering_calc[steering_info]
        throttle = 40
        command = 'DRIV{:04}{:04}'.format(throttle, steering)
        print (serial_no, offset, angle, command)
        print (my_pico.do_command(serial_no, command), '\n')
       
    time.sleep(0.005)
my_pico.do_command(serial_no, 'STOP')
print (module_name, 'finished')
