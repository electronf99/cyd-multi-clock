from machine import UART, Pin, I2C
from time import sleep
import time

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
    freq=400000
)

TMP117_ADDR = 0x48
RTC_ADDR = 0x52

print("I2C devices:", [hex(addr) for addr in i2c.scan()])



def bcd_to_dec(bcd):
    return ((bcd >> 4) * 10) + (bcd & 0x0F)

def dec_to_bcd(dec):
    return ((dec // 10) << 4) | (dec % 10)

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


def rv3028_get_time(i2c, addr):
    data = i2c.readfrom_mem(addr, 0x00, 7)

    second = bcd_to_dec(data[0] & 0x7F)
    minute = bcd_to_dec(data[1] & 0x7F)
    hour   = bcd_to_dec(data[2] & 0x3F)
    day    = bcd_to_dec(data[4] & 0x3F)
    month  = bcd_to_dec(data[5] & 0x1F)
    year   = 2000 + bcd_to_dec(data[6])

    return (year, month, day, hour, minute, second)


while True:

    temp = read_temperature(i2c, TMP117_ADDR)
    (year, month, day, hour, minute, second) = rv3028_get_time(i2c, RTC_ADDR)

    hhmm = f"{minute:02d}{second:02d}"
    brightness = 9
    packet = f"[{hhmm}{brightness}]\n" 
    uart.write(packet)

    print("Sent:", packet.strip())

    sleep(0.5)



 