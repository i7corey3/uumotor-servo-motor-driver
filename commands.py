import serial
import threading
from functions import *


class SerialHandler:
    def __init__(self, port, baud, timeout):
        self.port = port
        self.baud = baud
        self.timeout = timeout
        self.decodeBits = 16
        self.unsigned = False
        self.isEncoder = False
        self.encoderCount = 0
        self.data = b''

    def connect(self):
        self.ser = serial.Serial(port=self.port, baudrate=self.baud, timeout=self.timeout)
        self.terminate = False
        threading.Thread(target=self.read, args=(), daemon=False).start()

    def disconnect(self):
        self.ser.close()
        self.terminate = True

    def write(self, msg):
        self.ser.write(bytes.fromhex(msg))

    def read(self):
        while self.terminate is not True:
            d = self.ser.read(1)
            
            if d != b'\xee' and d != b'':
                d = b'\xee' + d
            d += self.ser.read_until(b'\xee')
            if len(d) > 1:
                if d[-1] == 238:
                    d = d[0:len(d)-1]
            
            if d != b'':
                if not self.isEncoder:
                    self.data = messageDecoder(d, self.decodeBits, self.unsigned)
                else:
                    
                    count = messageDecoder(d, self.decodeBits, self.unsigned)
                    if count != 1392508929 and count != "invalid message": 
                        self.encoderCount = count
                self.isEncoder = False

                
                    

class Commands:
    def __init__(self, model="svd6hs"):
        self.model = model
        self.params()

    def params(self):
        if self.model == "svd6hs":
            self.maxSpeed = 500
            self.maxAmp = 20
            self.torque = 20

    """
    Set Motor Parameters
    """
    
    def setControlMode(self, motor=1, mode="speed"):
        if mode == "speed":
            if motor == 1:
                return getHexMsg([0xee, 0x06, 0x51, 0x00, 0x00, 0x00])
            elif motor == 2:
                return getHexMsg([0xee, 0x06, 0x51, 0x01, 0x00, 0x00])
        elif mode == "position":
            if motor == 1:
                return getHexMsg([0xee, 0x06, 0x51, 0x00, 0x00, 0x01])
            elif motor == 2:
                return getHexMsg([0xee, 0x06, 0x51, 0x01, 0x00, 0x01])
        elif mode == "torque":
            if motor == 1:
                return getHexMsg([0xee, 0x06, 0x51, 0x00, 0x00, 0x02])
            elif motor == 2:
                return getHexMsg([0xee, 0x06, 0x51, 0x01, 0x00, 0x02])
        elif mode == "voltage":
            if motor == 1:
                return getHexMsg([0xee, 0x06, 0x51, 0x00, 0x00, 0x03])
            elif motor == 2:
                return getHexMsg([0xee, 0x06, 0x51, 0x01, 0x00, 0x03])
        elif mode == "skateboard":
            if motor == 1:
                return getHexMsg([0xee, 0x06, 0x51, 0x00, 0x00, 0x04])
            elif motor == 2:
                return getHexMsg([0xee, 0x06, 0x51, 0x01, 0x00, 0x04])
        elif mode == "karting":
            if motor == 1:
                return getHexMsg([0xee, 0x06, 0x51, 0x00, 0x00, 0x05])
            elif motor == 2:
                return getHexMsg([0xee, 0x06, 0x51, 0x01, 0x00, 0x05])
        else:
            print("invalid mode")

    def setLocationMode(self, motor=1, mode="absolute"):
        if mode == "absolute":
            if motor == 1:
                return getHexMsg([0xee, 0x06, 0x51, 0x04, 0x00, 0x00])
            elif motor == 2:
                return getHexMsg([0xee, 0x06, 0x51, 0x05, 0x00, 0x00])
        elif mode == "relative":
            if motor == 1:
                return getHexMsg([0xee, 0x06, 0x51, 0x04, 0x00, 0x01])
            elif motor == 2:
                return getHexMsg([0xee, 0x06, 0x51, 0x05, 0x00, 0x01])
    
    def setAccelerationMax(self, motor=1, value=0):
        if motor == 1:
            v = dec2hex(value, self.maxSpeed, unsigned=True)
            return getHexMsg([0xee, 0x06, 0x51, 0x08, v[0], v[1]])
        elif motor == 2:
            v = dec2hex(value, self.maxSpeed, unsigned=True)
            return getHexMsg([0xee, 0x06, 0x51, 0x0c, v[0], v[1]])
        else:
            print("invalid motor")

    def setDecelerationMax(self, motor=1, value=0):
        if motor == 1:
            v = dec2hex(value, self.maxSpeed, unsigned=True) 
            return getHexMsg([0xee, 0x06, 0x51, 0x09, v[0], v[1]])
        elif motor == 2:
            v = dec2hex(value, self.maxSpeed, unsigned=True)
            return getHexMsg([0xee, 0x06, 0x51, 0x0d, v[0], v[1]])
        else:
            print("invalid motor")
        
    def setSpeed(self, motor=1, speed=0):
        if motor == 1:
            v = dec2hex(speed, self.maxSpeed)
            return getHexMsg([0xee, 0x06, 0x53, 0x04, v[0], v[1]])
        elif motor == 2:
            v = dec2hex(speed, self.maxSpeed)
            return getHexMsg([0xee, 0x06, 0x53, 0x05, v[0], v[1]])
        else:
            print("invalid motor")
    
    def setCurrent(self, motor=1, current=0):
        if motor == 1:
            v = dec2hex(current/0.1, self.maxAmp)
            return getHexMsg([0xee, 0x06, 0x53, 0x08, v[0], v[1]]) 
        elif motor == 2:
            v = dec2hex(current/0.1, self.maxAmp)
            return getHexMsg([0xee, 0x06, 0x53, 0x09, v[0], v[1]]) 
        else:
            print("invalid motor")

    def sensorType(self, motor=1, type='hall'):
        if type == 'encoder':
            if motor == 1:
                return getHexMsg([0xee, 0x06, 0x50, 0x2c, 0x00, 0x00]) 
            elif motor == 2:
                return getHexMsg([0xee, 0x06, 0x50, 0x2d, 0x00, 0x00]) 
            else:
                print("invalid motor")
        elif type == 'hall':
            if motor == 1:
                return getHexMsg([0xee, 0x06, 0x50, 0x2c, 0x00, 0x01]) 
            elif motor == 2:
                return getHexMsg([0xee, 0x06, 0x50, 0x2d, 0x00, 0x01]) 
            else:
                print("invalid motor")
        elif type == 'string':
            if motor == 1:
                return getHexMsg([0xee, 0x06, 0x50, 0x2c, 0x00, 0x02]) 
            elif motor == 2:
                return getHexMsg([0xee, 0x06, 0x50, 0x2d, 0x00, 0x02]) 
            else:
                print("invalid motor")


    def controlMotor(self, motor=1, cmd="clear"):
        if cmd == "clear":
            if motor == 1:
                return getHexMsg([0xee, 0x06, 0x53, 0x00, 0x00, 0x02])
            elif motor == 2:
                return getHexMsg([0xee, 0x06, 0x53, 0x01, 0x00, 0x02])
        elif cmd == "stop":
            if motor == 1:
                return getHexMsg([0xee, 0x06, 0x53, 0x00, 0x00, 0x00])
            elif motor == 2:
                return getHexMsg([0xee, 0x06, 0x53, 0x01, 0x00, 0x00])
        elif cmd == "start":
            if motor == 1:
                return getHexMsg([0xee, 0x06, 0x53, 0x00, 0x00, 0x01])
            elif motor == 2:
                return getHexMsg([0xee, 0x06, 0x53, 0x01, 0x00, 0x01])
        else:
            print("invalid command")

    def calibrate(self, motor=1):
        if motor == 1:
            return getHexMsg([0xee, 0x06, 0x56, 0x00, 0x00, 0x01])
        elif motor == 2:
            return getHexMsg([0xee, 0x06, 0x55, 0x01, 0x00, 0x01])
        else:
            print("invalid motor")


    """
    Read Motor Status
    """

    def calibrationStatus(self, motor=1):
        if motor == 1:
            return getHexMsg([0xee, 0x03, 0x56, 0x84, 0x00, 0x01])
        elif motor == 2:
            return getHexMsg([0xee, 0x03, 0x55, 0x85, 0x00, 0x01])
        else:
            print("invalid motor")

    def motorRunning(self, motor=1):
        if motor == 1:
            return getHexMsg([0xee, 0x03, 0x54, 0x00, 0x00, 0x01])
        elif motor == 2:
            return getHexMsg([0xee, 0x03, 0x54, 0x01, 0x00, 0x01])
        else:
            print("invalid motor")
        
    def motorTemp(self, motor=1):
        if motor == 1:
            return getHexMsg([0xee, 0x03, 0x54, 0x04, 0x00, 0x01])
        elif motor == 2:
            return getHexMsg([0xee, 0x03, 0x54, 0x05, 0x00, 0x01])
        else:
            print("invalid motor")

    def busVoltage(self, motor=1):
        if motor == 1:
            return getHexMsg([0xee, 0x03, 0x54, 0x08, 0x00, 0x01])
        elif motor == 2:
            return getHexMsg([0xee, 0x03, 0x54, 0x09, 0x00, 0x01])
        else:
            print("invalid motor")

    def MOSTubeTemp(self, motor=1):
        if motor == 1:
            return getHexMsg([0xee, 0x03, 0x54, 0x0c, 0x00, 0x01])
        elif motor == 2:
            return getHexMsg([0xee, 0x03, 0x54, 0x0d, 0x00, 0x01])
        else:
            print("invalid motor")

    def motorSpeed(self, motor=1):
        if motor == 1:
            return getHexMsg([0xee, 0x03, 0x54, 0x10, 0x00, 0x01])
        elif motor == 2:
            return getHexMsg([0xee, 0x03, 0x54, 0x11, 0x00, 0x01])
        else:
            print("invalid motor")

    def motorCurrent(self, motor=1):
        if motor == 1:
            return getHexMsg([0xee, 0x03, 0x54, 0x14, 0x00, 0x01])
        elif motor == 2:
            return getHexMsg([0xee, 0x03, 0x54, 0x15, 0x00, 0x01])
        else:
            print("invalid motor")

    def absolutePosition(self, motor=1):
        if motor == 1:
            return getHexMsg([0xee, 0x03, 0x54, 0x18, 0x00, 0x01])
        elif motor == 2:
            return getHexMsg([0xee, 0x03, 0x54, 0x1a, 0x00, 0x01])
        else:
            print("invalid motor")

    def errorStatus(self, motor=1):
        if motor == 1:
            return getHexMsg([0xee, 0x03, 0x54, 0x20, 0x00, 0x01])
        elif motor == 2:
            return getHexMsg([0xee, 0x03, 0x54, 0x22, 0x00, 0x01])
        else:
            print("invalid motor")

    

    

    
    



