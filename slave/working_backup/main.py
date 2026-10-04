
# Rui Santos & Sara Santos - Random Nerd Tutorials
# Modified to fade the CYD backlight between image updates

from machine import Pin, SPI, PWM
from time import sleep, sleep_ms, ticks_ms, ticks_diff

from ili9341 import Display, color565
#from xglcd_font import XglcdFont

#import gc

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
    sleep(0.1)
    
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
    start = ticks_ms()
    fade_out()
    print("loadingb")
    display.draw_image(f"background.raw", 0, 0, 240,320)
    fade_in()
    print("loadingd")
    display.draw_image(f"nixie-{n}.raw", 0, 0, 240, 320)
    print("Draw:", ticks_diff(ticks_ms(), start), "ms")
    #fade_in()
    sleep(0.5)


try:



    # gc.collect()

    # start = ticks_ms()

    # with open("nixie-0.raw", "rb") as f:
    #     buf = bytearray(23040)   # current chunk size
    #     f.readinto(buf)

    # print("Read =", ticks_diff(ticks_ms(), start))

    while True:
        for digit in range(10):
            load_image(digit)
            sleep(0.3)

except Exception as e:
    print("Error occurred:", e)

except KeyboardInterrupt:
    print("Program interrupted by the user")

finally:
    backlight.duty_u16(65535)

