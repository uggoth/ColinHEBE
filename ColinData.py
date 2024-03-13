module_name = 'ColinData.py'

class ColinData():
    def __init__(self):
        self.params =  {'PI_NAME':'HEBE',
                        'ThisPi':'HEBE_V05',
                        'PICO_NAME':'PICOA',
                        'ColObjects':'ColObjects_Pi_V16',
                        'CommandStream':'CommandStreamPi_v06',
                        'GPIO':'GPIO_Pi_v47',
                        'AX12Servo':'AX12Servo_Pi_V01',
                        #  To obtain the AX12 port name use:    ls /dev/serial/by-id
                        'AX12_PATH':'/dev/ttyUSB0',
                        'AX12_SPEED':1000000,
                        'AX12_LIST':[20,21],
                        'BUZZER':[],
                        'LED':[]}

if __name__ == "__main__":
    print (module_name, 'starting')
    my_data = ColinData()
    import pprint
    pp = pprint.PrettyPrinter()
    pp.pprint(my_data.params)
    print (module_name, 'finished')
