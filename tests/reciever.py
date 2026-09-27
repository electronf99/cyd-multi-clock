
from machine import UART, Pin
from time import sleep_ms

uart = UART(
    1,
    baudrate=1200,
    rx=Pin(22),
    tx=Pin(21)   # unused, but UART wants a TX pin
)

print("Listening on GPIO22...")

while True:
    if uart.any():
        data = uart.readline()

        if data:
            try:
                print(f"---{data.decode().strip()}---")
            except:
                print(data)

    sleep_ms(10)
