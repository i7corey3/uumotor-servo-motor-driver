from functions import *

def dec2hex(dec, range, unsigned=False):
    if unsigned is False:
        actual = int(map_range(dec, -range, range, -32768, 32767))
    else:
        actual = int(map_range(dec, 0, range, 0, 65535))
    h = "{:04x}".format(int(actual))

    return [h[0:2], h[2:]]

print(dec2hex(200, 500, unsigned=True))