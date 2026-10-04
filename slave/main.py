
# Rui Santos & Sara Santos - Random Nerd Tutorials
# Modified to fade the CYD backlight between image updates

from machine import UART, Pin, SPI, PWM
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


def fade_out():
    for duty in range(32768, 8192, -32):
        backlight.duty_u16(duty)
    sleep(0.02)
    
    backlight.duty_u16(8192)
    # sleep(0.01)

def fade_in():
    for duty in range(2048, 16384, 32):
        backlight.duty_u16(duty)
        sleep_ms(2)

    # Ensure full brightness
    backlight.duty_u16(16384)


def load_image(n):
    #fade_out()
    #fade_out()
    display.draw_image(f"background.raw", 0, 0, 240,320)
    display.draw_image(f"nixie-{n}.raw", 0, 0, 240, 320)
    #fade_in()
    

    


uart = UART(
    1,
    baudrate=115200,
    rx=Pin(22),
    tx=Pin(21)   # unused, but UART wants a TX pin
)



with open("DIGITNUM", "r") as f:
    DIGITNUM = int(f.read().strip())

last_digit = 0

print("Listening on GPIO22...")
try:
    while True:
        if uart.any():
            data = uart.readline()

            if data:
                try:
                    rx = data.decode().strip()
                    #print(list(rx)[5])
                    digit = list(rx)[DIGITNUM]                    
                    if list(rx)[0] == "[" and list(rx)[5] == "]":
                        print(rx)
                        if last_digit != digit:
                            print(f"{rx} -> {digit}")
                            number = rx
                            load_image(digit)
                            last_digit=digit
                    else:
                        print("data error")
                except:
                    print("##")

        sleep_ms(100)

except Exception as e:
    print("Error occurred:", e)

except KeyboardInterrupt:
    print("Program interrupted by the user")

finally:
    backlight.duty_u16(65535)

