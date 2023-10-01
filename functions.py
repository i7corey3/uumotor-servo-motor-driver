
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
    
  
def map_range(x, in_min, in_max, out_min, out_max):
    if x > in_max:
        return out_max
    elif x < in_min:
        return out_min
    else:
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def dec2hex(dec, range, unsigned=False):
    if unsigned is False:
        actual = int(map_range(dec, -range, range, -32768, 32767))
        h = hex( (actual & 0xffff))
    else:
        actual = int(map_range(dec, 0, range, 0, 65535))
    
        h = "0x{:02x}".format(actual)

    high, low = divmod(int(h,16), 0x100)
   
    return [high, low]

def checkSum(msg):
    try:
        crc = 0xFFFF
        bitmsg = []
        for i in range(0, len(msg)-2):
            bitmsg.append(int(msg[i]))
        crc = msg[-2] << 8 & crc | msg[-1]
        check = calculate_crc16(bitmsg)

        if check == crc:
            return True
        else:
            return False
    except IndexError:
        return False

def messageDecoder(msg, bit, unsigned):
    # print(msg, checkSum(msg), len(msg))
    if checkSum(msg) == False:
        return "invalid message"
    else:
        if bit == 16:
            msg = msg[0:-2]
            data = 0xFFFF
            data = msg[-2] << 8 & data | msg[-1]
            if unsigned == False:
                data = (data & 0xffff)


            return data
        
        elif bit == 32:
            data = 0xFFFFFFFF
            msg = msg[0:-2]
            # try:
            #     print(hex(msg[0]), hex(msg[1]), hex(msg[2]), hex(msg[3]), hex(msg[4]), hex(msg[5]), hex(msg[6]))
            # except:
            #     pass
            data = (msg[-4] << 24 & data) | (msg[-3] << 16 & data) | (msg[-2] << 8 & data) | msg[-1] 
            if unsigned == False:
                data = (data & 0xFFFFFFFF)
                return (data ^ 0x80000000) - 0x80000000
            else:

                return data


if __name__ == "__main__":
    val = 20
    v = dec2hex(val, 500, True)
    for i in v:
        print(hex(i))
