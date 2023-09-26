
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


    
if __name__ == "__main__":
    val = -10
    print(dec2hex(val, 500))
