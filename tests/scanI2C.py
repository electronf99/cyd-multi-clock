from machine import I2C, Pin
from time import sleep

i2c = I2C(
    0,
    scl=Pin(12),
    sda=Pin(11),
    freq=400_000
)

print("Scanning I2C bus...")

while True:
    devices = i2c.scan()

    if devices:
        print("Found {} device(s):".format(len(devices)))

        for addr in devices:
            print(
                "Decimal: {:3d}  Hex: 0x{:02X}".format(
                    addr,
                    addr
                )
            )
    else:
        print("No I2C devices found")
    sleep(0.5)