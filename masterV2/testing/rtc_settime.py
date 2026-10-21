from machine import UART, Pin, I2C
from time import sleep
import time
from Makerverse_RV3028 import Makerverse_RV3028

i2c = I2C(
    0,
    sda=Pin(11),
    scl=Pin(12),
    freq=400000
)

TMP117_ADDR = 0x48

def read_temperature(i2c, addr):
    
    data = i2c.readfrom_mem(addr, 0x00, 2)
    
    # Shift 1st byte left and or with 2nd byte)
    raw = (data[0] << 8) | data[1]
        
    # Convert from signed 16-bit
    if raw & 0x8000:
        raw -= 65536

    temp_c = raw / 128    
    return temp_c


rtc = Makerverse_RV3028(i2c = i2c)

print(rtc.timestamp())

ymd = [20,10,11]
#rtc.setDate(ymd)

hms = [17,44,0]
#rtc.setTime(hms)
while True:
    print(f"{rtc.timestamp()} : {read_temperature(i2c, TMP117_ADDR):2.1f}")
    sleep(1)