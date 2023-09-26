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
        self.motor1Param = ["speed", 200, -200, 2]
        self.terminate = False
        time.sleep(2)
        threading.Thread(target=self.controlMotors, args=(), ).start()


    def controlMotors(self):
        self.driver.setMotorParameters(1, self.motor1Param[0], self.motor1Param[1], self.motor1Param[2], self.motor1Param[3])
        while not self.terminate:   
            if self.cmd == "changeSpeed":
                self.driver.setMotorSpeed(1, self.motorSpeed)
            if self.runMotor:
                self.driver.driveMotor(1)
            self.cmd = ""
            time.sleep(0.1)

    def changeSpeed(self, motor, speed):
        if motor == 1:
            self.cmd = "changeSpeed"
            self.motorSpeed = speed

    def stopMotor(self, motor):
        if motor == 1:
            self.runMotor = False
        
    def startMotor(self, motor):
        if motor == 1:
            self.runMotor = True

if __name__ == "__main__":
    control = Controller("/dev/ttyUSB0", 115200, 1)
    while True:
        c = input("""
Motor Controller Test
Type start to run motor,
Type stop to stop motor,
Type changeSpeed (value) to change speed,
Type quit to quit
            """).split(" ")
        print(c)
        try:
            if c[0] == "start":
                control.startMotor(1)
            elif c[0] == "stop":
                control.stopMotor(1)
            elif c[0] == "changeSpeed":
                control.changeSpeed(1, int(c[1]))
            elif c[0] == "quit":
                control.driver.driver.disconnect
                control.terminate = True
                break
        except:
            pass
    