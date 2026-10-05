
from machine import Pin, I2C
from time import sleep, sleep_ms, ticks_ms, ticks_diff
import time


##### Used to set RTC time. 
##### Thonny sets the system time so connect and run from there
##### 


i2c = I2C(
    0,
    sda=Pin(11),
    scl=Pin(12),
    freq=400000
)

def bcd_to_dec(bcd):
    return ((bcd >> 4) * 10) + (bcd & 0x0F)

def dec_to_bcd(dec):
    return ((dec // 10) << 4) | (dec % 10)


def update_rv3028_from_system_clock(i2c, addr=0x52):
    year, month, day, hour, minute, second, weekday, yearday = time.localtime()

    print(f"Setting RTC to "
          f"{year:04d}-{month:02d}-{day:02d} "
          f"{hour:02d}:{minute:02d}:{second:02d}")

    data = bytes([
        dec_to_bcd(second),
        dec_to_bcd(minute),
        dec_to_bcd(hour),
        dec_to_bcd(weekday + 1),
        dec_to_bcd(day),
        dec_to_bcd(month),
        dec_to_bcd(year % 100)
    ])

    i2c.writeto_mem(addr, 0x00, data)



def rv3028_get_time(i2c, addr):
    data = i2c.readfrom_mem(addr, 0x00, 7)

    second = bcd_to_dec(data[0] & 0x7F)
    minute = bcd_to_dec(data[1] & 0x7F)
    hour   = bcd_to_dec(data[2] & 0x3F)
    day    = bcd_to_dec(data[4] & 0x3F)
    month  = bcd_to_dec(data[5] & 0x1F)
    year   = 2000 + bcd_to_dec(data[6])

    return (year, month, day, hour, minute, second)


#update_rv3028_from_system_clock(i2c)


#
    # sec = i2c.readfrom_mem(0x52, 0x00, 1)[0]
    # print(hex(sec))

# Set RTC from ESP32 clock
year, month, day, hour, minute, second, weekday, yearday = time.localtime()

rv3028_set_time(
    i2c,
    year,
    month,
    day,
    hour,
    minute,
    second,
    weekday + 1
)
return 0

val = i2c.readfrom_mem(0x52, 0x37, 1)[0]

print("Before:", hex(val))

val |= 0x20     # Set bit 5

i2c.writeto_mem(0x52, 0x37, bytes([val]))

val = i2c.readfrom_mem(0x52, 0x37, 1)[0]
print("After :", hex(val))


# for reg in [0x0D, 0x0E, 0x0F]:
#     val = i2c.readfrom_mem(0x52, reg, 1)[0]
#     print(hex(reg), hex(val))

print(rv3028_get_time(i2c, 0x52))

# for reg in [0x37, 0x38, 0x39]:
#     print(hex(reg), hex(i2c.readfrom_mem(0x52, reg, 1)[0]))
        
    #sleep(1)

from machine import Pin, I2C
from time import sleep
import time

i2c = I2C(
    0,
    sda=Pin(11),
    scl=Pin(12),
    freq=400000
)

RTC_ADDR = 0x52


def dec_to_bcd(dec):
    return ((dec // 10) << 4) | (dec % 10)


def rv3028_set_time(i2c, year, month, day,
                    hour, minute, second,
                    weekday=1, addr=0x52):

    data = bytes([
        dec_to_bcd(second),
        dec_to_bcd(minute),
        dec_to_bcd(hour),
        dec_to_bcd(weekday),
        dec_to_bcd(day),
        dec_to_bcd(month),
        dec_to_bcd(year % 100)
    ])

    i2c.writeto_mem(addr, 0x00, data)


# Enable trickle charger
val = i2c.readfrom_mem(RTC_ADDR, 0x37, 1)[0]
val |= 0x20
i2c.writeto_mem(RTC_ADDR, 0x37, bytes([val]))

print("Backup register:", hex(i2c.readfrom_mem(RTC_ADDR, 0x37, 1)[0]))

# Clear status flags
i2c.writeto_mem(RTC_ADDR, 0x0E, b"\x00")

from machine import Pin, I2C

i2c = I2C(0, sda=Pin(11), scl=Pin(12))

val = i2c.readfrom_mem(0x52, 0x37, 1)[0]

# Enable battery/supercap switchover
val &= ~0x0C
val |= 0x04

# Enable trickle charger
val |= 0x20

i2c.writeto_mem(0x52, 0x37, bytes([val]))

print("0x37 =", hex(i2c.readfrom_mem(0x52, 0x37, 1)[0]))

# Set RTC from ESP32 clock
year, month, day, hour, minute, second, weekday, yearday = time.localtime()

rv3028_set_time(
    i2c,
    year,
    month,
    day,
    hour,
    minute,
    second,
    weekday + 1
)




