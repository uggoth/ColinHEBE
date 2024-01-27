module_name = 'test_15_F_command_stream_v01.py'
print (module_name,'starting')
print ('expects test_15_F to be running on the Pico')

import CommandStreamPi_v03 as CommandStream
import time
import pigpio

gpio = pigpio.pi()
handshake = CommandStream.Handshake(4, gpio)
pico_id = 'PICOA'
my_pico = CommandStream.Pico(pico_id, gpio, handshake)

if my_pico.valid:
    msgs = ['DUMMY','WHOU','DUMMY','MFWD0050',
            'DUMMY','MSTP','DUMMY','EXIT']
    for msg in msgs:
        print (' ')
        print (msg)
        time.sleep(1)
        print (my_pico.do_command(msg))
else:
    print ('*** No Pico')
my_pico.close()
print (module_name, 'finished')
