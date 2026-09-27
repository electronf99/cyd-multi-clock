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

    hhmm = "{:02d}{:02d}\n".format(
        t[3],  # hour
        t[4]  # minute
    )

    uart.write(hhmm)

    print("Sent:", hhmm.strip())

    sleep(0.5)


