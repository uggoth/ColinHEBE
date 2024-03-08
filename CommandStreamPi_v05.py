module_name = 'CommandStreamPi_v05.py'
last_modified = '30/Jan/2024'
if __name__ == "__main__":
    print (module_name, 'starting')

import pigpio
import time
import serial, sys, select

class Handshake():
    def __init__(self, pin_no, gpio):
        self.pin_no = pin_no
        self.gpio = gpio
        self.gpio.set_mode(pin_no, pigpio.INPUT)
        self.gpio.set_pull_up_down(pin_no, pigpio.PUD_UP)
    def get(self):
        return self.gpio.read(self.pin_no)
    def wait(self):
        for i in range(1000):
            check = self.get()
            if check == 1:
                return True
            else:
                time.sleep(0.001)
        print ('handshake not set after',i,'iterations')
        return False

class Pico():

    def __init__(self, pico_id, gpio, handshake):

        self.possible_picos = {'SHEEP':'Sheep Pico',
                               'TROUGH':'Trough Pico',
                               'HORSE':'Dummy Test Pico',
                               'PICKER':'Apple Picker',
                               'MOTOR':'Motor Pico',
                               'TYPICAL':'Test Pico',
                               'PICOF':'Pico F',
                               'PICOA':'Pico A',
                               'PICOR':'Pico R (ZyderBot)',
                               'PS3':'Remote Control ESP32'}
        self.possible_ports = ['/dev/ttyACM0',
                               '/dev/ttyACM1',
                               '/dev/ttyACM2',
                               '/dev/ttyACM3',
                               '/dev/ttyUSB00',
                               '/dev/ttyUSB01']
        self.id = pico_id
        self.gpio = gpio
        self.handshake = handshake
        self.port_name = 'Unknown'
        self.name = 'Unknown'
        self.description = 'Unknown'
        self.port = None
        self.valid = False

        if pico_id not in self.possible_picos:
            print ('**** ',pico_id,'not known')
            return
        
        for possible_port in self.possible_ports:
            time.sleep(0.01)
            try:
                test_port = serial.Serial(possible_port,
                                          timeout=0.1,
                                          write_timeout=0.1,
                                          baudrate=115200)
            except:
                print (possible_port,'failed to open')
                continue
            print (possible_port,'opened OK')
            self.port = test_port
            if not self.send('0000WHOU'):
                print ('**** WHOU send failed')
                self.port.close
                continue
            time.sleep(0.001)
            result = self.get(2)
            if result:
                print ('Received:', result)
                if len(result) < 9:
                    print ('Bad name: ', result)
                    self.port.close
                    continue
                pico_name = result[8:]
                if not pico_name:
                    print ('**** WHOU get failed')
                    self.port.close
                    continue
                if pico_name not in self.possible_picos:
                    print ('**** Pico', pico_name, 'not in list')
                    continue
                print ('Pico name:', pico_name, self.possible_picos[pico_name])
                if pico_name == pico_id:
                    self.description = self.possible_picos[pico_id]
                    self.name = pico_id
                    self.port_name = possible_port
                    self.valid = True
                    break
                else:
                    print ("Unexpectedly got '{}'".format(result))
                    self.name = 'UNKNOWN'
                    self.id = 'UNKNOWN'
                    self.port.close
                    continue
        print ('Pico Init Done')

    def __str__(self):
        return self.name

    def send(self, text):  #  Don't use directly. Use do_command
        in_text = text + '\n'
        out_text = in_text.encode('utf-8')
        try:
            self.port.write(out_text)
        except:
            print ('write failed')
            return False
        return True

    def get(self, timeout=0.02):  #  Don't use directly. Use do_command
        inputs, outputs, errors = select.select([self.port],[],[],timeout)
        if len(inputs) > 0:
            read_text = self.port.readline()
            decoded_text = read_text.decode('utf-8')[:-2]
            return decoded_text
        else:
            return False

    def flush(self):
        more = 1
        timeout=0.001
        flushed = 0
        while more > 0:
            inputs, outputs, errors = select.select([self.port],[],[],timeout)
            more = len(inputs)
            if more > 0:
                discard = self.port.readline()
                flushed += 1
        return flushed

    def do_command(self, serial_no, command):
        #print ('Executing',command)
        if self.handshake is not None:
            result = self.handshake.wait()
        else:
            result = True
        if result:
            #print ('handshake OK')
            success = self.send(serial_no + command)
            if success:
                #print ('send OK')
                reply = self.get()
                if not reply:
                    return serial_no, 'BADG', reply
                if len(reply) < 8:
                    return serial_no, 'BADL', reply
                serial_no = reply[0:4]
                feedback = reply[4:8]
                if len(reply) > 8:
                    data = reply[8:]
                else:
                    data = None
                return serial_no, feedback, data
            else:
                return serial_no, 'BADS', reply
        else:
            return serial_no, 'BADH', reply

    def close(self):
        if self.port:
            self.port.close()

class TypicalUsage(Pico):
    def __init__(self):
        self.gpio = pigpio.pi()
        self.handshake = Handshake(17, self.gpio)
        my_name = 'PICOF'
        super().__init__(my_name, self.gpio, self.handshake)
        if not self.id == my_name:
            print ('**** initialisation failed for pico', my_name)
        
if __name__ == "__main__":
    print (module_name, 'finished')
