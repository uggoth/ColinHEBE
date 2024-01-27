module_name = 'ColinData.py'

class ColinData():
    def __init__(self):
        self.params =  {'PI_NAME':'HEBE',
                        'ThisPi':'HEBE_V01',
                        'ColObjects':'ColObjects_Pi_V15',
                        'CommandStream':'CommandStreamPi_v02',
                        'GPIO':'GPIO_Pi_v46',
                        'AX12Servo':'AX12Servo_Pi_V01',
                        #  To obtain the AX12 port name use:    ls /dev/serial/by-id
                        'AX12_PATH':'/dev/serial/by-id/usb-FTDI_USB__-__Serial_Converter_FT4TCJWH-if00-port0',
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
