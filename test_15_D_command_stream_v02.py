module_name = 'test_15_D_command_stream_v01.py'
print (module_name,'starting')
print ('expects test_15_D to be running on the Pico')

import CommandStreamPi_v05 as CommandStream
import time
import pigpio

gpio = pigpio.pi()
handshake = CommandStream.Handshake(4, gpio)
pico_id = 'PICOA'
my_pico = CommandStream.Pico(pico_id, gpio, handshake)
i = 0
if my_pico.valid:
    msgs = ['TEST1','WHOU','TEST2','TEST3','TEST4','TEST5','EXIT']
    for msg in msgs:
        time.sleep(1)
        print (msg, my_pico.send(msg))
else:
    print ('*** No Pico')
my_pico.close()
print (module_name, 'finished')
