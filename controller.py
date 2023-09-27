from motor_control import MotorControl
import threading
import time

class Controller:
    def __init__(self, port, baud, timeout):
        self.port = port
        self.baud = baud
        self.timeout = timeout
        self.driver = MotorControl(self.port, self.baud, self.timeout)
        self.cmd = ""
        self.runMotor = False
        self.motorSpeed = 10
        self.motor1Param = ["speed", 200, -200, 2, "hall"]
        self.terminate = False
        self.calibrate = False
        time.sleep(2)
        threading.Thread(target=self.controlMotors, args=(), ).start()


    def controlMotors(self):
        self.driver.setMotorParameters(1, self.motor1Param[0], self.motor1Param[1], self.motor1Param[2], self.motor1Param[3], self.motor1Param[4])
        
        time.sleep(0.1)
        while not self.terminate:   
            if self.cmd == "changeSpeed":
                self.driver.setMotorSpeed(1, self.motorSpeed)
                time.sleep(0.1)
            if self.runMotor:
                self.driver.driveMotor(1)
                print(self.getAbsolutePosition(1))
            if self.calibrate:
                if self.driver.calibrationStatus(1) == 0:
                    print("Calibration Complete")
                    self.calibrate = False
                elif self.driver.calibrationStatus(1) == 2:
                    print("Calibration Failed")
                    self.calibrate = False
                else:
                    print("Calibrating")
                
                #print((self.driver.errorStatus(1)))
            self.cmd = ""
            time.sleep(0.1)

    def changeSpeed(self, motor, speed):
        if motor == 1:
            self.cmd = "changeSpeed"
            self.motorSpeed = speed

    def changeCurrent(self, motor, current):
        if motor == 1:
            self.driver.changeCurrent(motor, current)

    def stopMotor(self, motor):
        if motor == 1:
            self.runMotor = False
        
    def startMotor(self, motor):
        if motor == 1:
            self.runMotor = True

    def motorRunning(self, motor):
        if motor == 1:
            return self.driver.motorRunning(1)
    
    def readTemp(self, motor):
        if motor == 1:
            return self.driver.readTemp(1)
        
    def readVolt(self, motor):
        if motor == 1:
            return self.driver.readVolt(1)
        
    def getAbsolutePosition(self, motor):
        if motor == 1:
            return self.driver.getAbsPosition(motor)
        
    def calibrateMotor(self, motor):
        if motor == 1:
            self.runMotor = False
            self.driver.calibrate(1)
            time.sleep(2)
            self.calibrate = True

if __name__ == "__main__":
    control = Controller("/dev/ttyUSB0", 115200, 1)
    while True:
        c = []
        c = input("""
Motor Controller Test
Type ca to calibrate,
Type s to run motor,
Type x to stop motor,
Type cs (value) to change speed,
Type cc (value) to change the current,
Type mr to check if motor is running,
Type rt to read motor temp,
Type rv to read bus voltage,
Type ap to read absolute position,
Type q to quit
            """).split(" ")
        try:

            if c[0] == 'ca':
                control.calibrateMotor(1)
            elif c[0] == "s":
                control.startMotor(1)
            elif c[0] == "x":
                control.stopMotor(1)
            elif c[0] == "cs":
                control.changeSpeed(1, int(c[1]))
            elif c[0] == "cc":
                control.changeCurrent(1, int(c[1]))
            elif c[0] == 'mr':
                print(control.motorRunning(1))
            elif c[0] == 'rt':
                print(control.readTemp(1))
            elif c[0] == 'rv':
                print(control.readVolt(1))
            elif c[0] == 'ap':
                print(control.getAbsolutePosition(1))
            elif c[0] == "q":
                control.driver.driver.disconnect
                control.terminate = True
                break
        except:
            pass
    