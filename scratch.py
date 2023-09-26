import serial
import time

def calculate_crc16(data):
    crc = 0xFFFF
    polynomial = 0xA001

    for byte in data:
        crc ^= byte
        for _ in range(8):
            if crc & 0x0001:
                crc = (crc >> 1) ^ polynomial
            else:
                crc >>= 1

    return crc

def getHexMsg(data):
    finalStr = ""
    calCrc = calculate_crc16(data)
    high, low = divmod(calCrc, 0x100)
    data.append(high)
    data.append(low)
    data = list(("{:02x}".format(i) for i in data))
    for i in data:
        finalStr = finalStr + i + " "
    return finalStr

    #


ser = serial.Serial(port="/dev/ttyUSB0", baudrate=115200, timeout=1)
dataByte = [0xEE, 0x06, 0x51, 0x00, 0x00, 0x00]

msg = []
hexBytes = []

print(hexBytes)
# set to speed control
msg.append(getHexMsg([0xEE, 0x06, 0x51, 0x00, 0x00, 0x00]))
# set speed
msg.append(getHexMsg([0xEE, 0x06, 0x53, 0x04, 0x0F, 0x00]))
# set current
msg.append(getHexMsg([0xEE, 0x06, 0x53, 0x08, 0x00, 0x14]))
# run motor
msg.append(getHexMsg([0xEE, 0x06, 0x53, 0x00, 0x00, 0x02]))
msg.append(getHexMsg([0xEE, 0x06, 0x53, 0x00, 0x00, 0x01]))


#msg = "EE 06 54 10 00 01 60 83"
for i in msg:
    ser.write(bytes.fromhex(i))
    time.sleep(0.1)

# ser.write(bytes.fromhex((hexBytes[0])))

while True:
    message = ser.readall()
    print(message)