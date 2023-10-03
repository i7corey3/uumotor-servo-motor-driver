from commands import SerialHandler, Commands
import time


class MotorControl:
    def __init__(self, port, baud, timeout=1):
        self.port = port
        self.baud = baud
        self.timeout = timeout
        self.command = Commands()
        self.driver = SerialHandler(self.port, self.baud, self.timeout)
        self.driver.connect()
        # time.sleep(1)
        # self.driver.write(self.command.controlMotor(1, "clear"))
        # self.driver.write(self.command.controlMotor(2, "clear"))
  
    def driveMotor(self, motor):
        self.driver.write(self.command.controlMotor(motor, "start"))

    def setMotorParameters(self, motor, controlMode, maxSpeed, minSpeed, maxAmp, sensor):
        self.driver.write(self.command.setControlMode(motor, controlMode))
        self.driver.write(self.command.setAccelerationMax(motor, maxSpeed))
        self.driver.write(self.command.setDecelerationMax(motor, minSpeed))
        self.driver.write(self.command.setCurrent(motor, maxAmp))
        self.driver.write(self.command.sensorType(motor, sensor))
        
    def changeCurrent(self, motor, current):
        self.driver.write(self.command.setCurrent(motor, current))


    def setMotorSpeed(self, motor, speed):
        self.driver.write(self.command.controlMotor(motor, "clear"))
        self.driver.write(self.command.setSpeed(motor, speed))
        
 
    def stopMotor(self, motor):
        self.driver.write(self.command.controlMotor(motor, "stop"))

    def motorRunning(self, motor):
        self.driver.unsigned = True
        self.driver.decodeBits = 16
        self.driver.write(self.command.motorRunning(motor))
        time.sleep(0.01)
        if self.driver.data == 1:
            return True
        else:
            return False
        
    def readTemp(self, motor):
        self.driver.unsigned = False
        self.driver.decodeBits = 16
        self.driver.write(self.command.motorTemp(motor))
        time.sleep(0.01)
        
        return self.driver.data/0.1
    
    def readVolt(self, motor):
        self.driver.unsigned = False
        self.driver.decodeBits = 16
        self.driver.write(self.command.busVoltage(motor))
        time.sleep(0.01)

        return self.driver.data*0.1
    
    def getAbsPosition(self, motor):
        self.driver.isEncoder = True
        self.driver.unsigned = False
        self.driver.decodeBits = 32
        self.driver.write(self.command.absolutePosition(motor))
        time.sleep(0.01)

        return self.driver.encoderCount



    def calibrate(self, motor):
        self.driver.write(self.command.calibrate(motor))
    
    def calibrationStatus(self, motor):
        self.driver.unsigned = True
        self.driver.decodeBits = 16
        self.driver.write(self.command.calibrationStatus(motor))
        time.sleep(0.01)
        
        return self.driver.data
        
    def errorStatus(self, motor):
        self.driver.unsigned = False
        self.driver.decodeBits = 32
        self.driver.write(self.command.errorStatus(motor))
        time.sleep(0.01)

        return self.driver.data

if __name__ == "__main__":
    driver = MotorControl("/dev/ttyUSB0", 115200, 1)
    # driver.calibrate(1)
    
    driver.setMotorParameters(1, "speed", 100, -100, 2)
    driver.driveMotor(1)

        

        