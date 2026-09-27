
from machine import UART, Pin
from time import sleep
import time

uart = UART(
    1,
    baudrate=115200,
    tx=Pin(5),
    rx=Pin(6)
)

while True:
    t = time.localtime()

    hhmmss = "{:02d}{:02d}{:02d}\n".format(
        t[3],  # hour
        t[4],  # minute
        t[5]   # second
    )

    uart.write(hhmmss)

    print("Sent:", hhmmss.strip())

    sleep(0.5)
