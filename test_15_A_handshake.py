#  Test command stream handshake
#  Run in conjunction with test_15_A... on the Pico

module_name = 'test_15_A_handshake.py'
print (module_name, 'starting')

import time
start_time = time.time()
import pigpio

handshake_pin = 4
gpio = pigpio.pi()
gpio.set_pull_up_down(handshake_pin, pigpio.PUD_UP)
previous = gpio.read(handshake_pin)
for i in range(900):
    new = gpio.read(handshake_pin)
    if new != previous:
        print (new)
        previous = new
    time.sleep(0.01)

gpio.stop()
print (module_name, 'finished')
