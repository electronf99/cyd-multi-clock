from machine import UART, Pin, I2C
from time import sleep
import time
from Makerverse_RV3028 import Makerverse_RV3028

uart = UART(
    1,
    baudrate=115200,
    tx=Pin(42),
    rx=Pin(41)
)
DEBUG=0

i2c = I2C(
    0,
    sda=Pin(11),
    scl=Pin(12),
    freq=40_000
)

TMP117_ADDR = 0x48


print("I2C devices:", [hex(addr) for addr in i2c.scan()])

rtc = Makerverse_RV3028(i2c = i2c)

# Read Temperature from I2C TMP117 device
# Data consists of 2 bytes. data[0] is msb
# The TMP117 datasheet defines each register bit as 0.0078125°C per LSB.
# Shift byte 1 left and or with byte 2
# 
def read_temperature(i2c, addr):
    
    data = i2c.readfrom_mem(addr, 0x00, 2)
    
    # Shift 1st byte left and or with 2nd byte)
    raw = (data[0] << 8) | data[1]
        
    # Convert from signed 16-bit
    if raw & 0x8000:
        raw -= 65536

    temp_c = raw / 128    
    return temp_c


def rv3028_get_time(rtc):

    (year, month, day) = (rtc.getDate(timeFormat='list'))
    (hour, minute, second) = (rtc.getTime(timeFormat='list'))
    return (year, month, day, hour, minute, second)

count=0

while True:

    temp = read_temperature(i2c, TMP117_ADDR)
    (year, month, day, hour, minute, second) = rv3028_get_time(rtc)

    hhmm = f"{hour:02d}{minute:02d}"
    brightness = 8

    temp_packet = f"[{int(temp*10):03d}C{brightness}]"
    time_packet = f"[{hhmm}{brightness}]"

    print(f"{rtc.timestamp()} : {temp} ")

    if second % 10 == 9 or second % 10 == 8:
        packet = temp_packet
    else:
        packet = time_packet    
    

    uart.write(packet + "\n")

    print("Sent:", packet.strip())

    sleep(0.5)



 