
# Rui Santos & Sara Santos - Random Nerd Tutorials
# Modified to fade the CYD backlight between image updates

import machine
from machine import UART, Pin, SPI, PWM, WDT
from time import sleep, sleep_ms, ticks_ms, ticks_diff
from ili9341 import Display, color565

import random

# pyright: reportAttributeAccessIssue=false

uart = UART(
    1,
    baudrate=115200,
    rx=Pin(22),
    tx=Pin(5)   # unused, but UART wants a TX pin
)


# TFT display SPI
display_spi = SPI(
    1,
    baudrate=80000000,
    sck=Pin(14),
    mosi=Pin(13)
)

# TFT display
display = Display(
    display_spi,
    dc=Pin(2),
    cs=Pin(15),
    rst=Pin(15),
    width=240,
    height=320,
    rotation=270
)

# Colours
white_color = color565(255, 255, 255)
black_color = color565(0, 0, 0)

# PWM backlight control
backlight = PWM(Pin(21))
backlight.freq(1000)
backlight.duty_u16(65535)  # full brightness

def load_image(n):
    display.draw_image(f"background.raw", 0, 0, 240,320)
    display.draw_image(f"nixie-{n}.raw", 0, 0, 240, 320)


def set_brightness(brightness):
    duty=int(65535 / (10 - int(brightness)))
    print(f"duty: {duty}")
    backlight.duty_u16(duty)


with open("DIGITNUM", "r") as f:
    DIGITNUM = int(f.read().strip())

last_digit = 0

set_brightness(9)
display.draw_image(f"background.raw", 0, 0, 240,320)

print("Listening on GPIO22...")

print("Setting Watchdog Timer")
wdt = WDT(timeout=10000) # 10 seconds

try:
    while True:
        wdt.feed()
        if uart.any():
            data = uart.readline()

            if data:
                print(data)
                rx = data.decode().strip()
                try:
                    rx = data.decode().strip()
                    #print(list(rx)[5])
                    digit = list(rx)[DIGITNUM]
                    
                 
                    if(len(rx) == 7):
                        if list(rx)[0] == "[" and list(rx)[6] == "]":

                            brightness = (list(rx)[5])
                            print(brightness)
                            set_brightness(brightness)
                            print(f"digit: {digit}")   

                            if last_digit != digit:
                                print(f"{rx} -> {digit}")
                                number = rx
                                load_image(digit)
                                last_digit=digit
                        else:
                            print("data error")
                    else:
                        print(f"only received {len(rx)}")
                except Exception as e:
                    print("##")
                    print(e)

        sleep_ms(100)

except Exception as e:
    print("Error occurred:", e)
    machine.reset()

except KeyboardInterrupt:
    print("Program interrupted by the user")

finally:
    backlight.duty_u16(65535)

