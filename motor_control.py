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

    def setMotorParameters(self, motor, controlMode, maxSpeed, minSpeed, maxAmp):
        self.driver.write(self.command.setControlMode(motor, controlMode))
        self.driver.write(self.command.setAccelerationMax(motor, maxSpeed))
        self.driver.write(self.command.setDecelerationMax(motor, minSpeed))
        self.driver.write(self.command.setCurrent(motor, maxAmp))


    def setMotorSpeed(self, motor, speed):
        self.driver.write(self.command.controlMotor(motor, "clear"))
        self.driver.write(self.command.setSpeed(motor, speed))
        
 
    def stopMotor(self, motor):
        self.driver.write(self.command.controlMotor(motor, "stop"))


    def calibrate(self, motor):
        self.driver.write(self.command.calibrate(motor))
        time.sleep(1)
        self.driver.write(self.command.calibrationStatus(motor))
        time.sleep(1)
        print(self.driver.data)


if __name__ == "__main__":
    driver = MotorControl("COM4", 115200, 1)
    # driver.calibrate(1)
    
    driver.setMotorParameters(1, "speed", 100, -100, 2)
    driver.driveMotor(1)

        

        