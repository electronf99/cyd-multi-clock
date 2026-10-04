from machine import UART, Pin
from time import sleep
import time

uart = UART(
    1,
    baudrate=115200,
    tx=Pin(40),
    rx=Pin(6)
)

while True:
    t = time.localtime()

    hhmm = "{:02d}{:02d}".format(
        t[3],  # hour
        t[4]  # minute
    )
    packet = f"[{hhmm}]\n" 
    uart.write(packet)

    print("Sent:", packet.strip())

    sleep(0.5)


