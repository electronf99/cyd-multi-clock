
# Rui Santos & Sara Santos - Random Nerd Tutorials
# Modified to fade the CYD backlight between image updates

from machine import Pin, SPI, PWM, SDCard
from time import sleep, sleep_ms, ticks_ms, ticks_diff
import os
import gc

from ili9341 import Display, color565

import random



sd = SDCard(slot=2)

os.mount(sd, "/sd")



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
backlight.duty_u16(16384)  # full brightness


def fade_out():
    for duty in range(16384, 8192, -32):
        backlight.duty_u16(duty)
    sleep(0.02)
    
    backlight.duty_u16(8192)
    # sleep(0.01)

def fade_in():
    for duty in range(2048, 16384, 32):
        backlight.duty_u16(duty)
        #sleep_ms(2)

    # Ensure full brightness
    backlight.duty_u16(16384)


def load_image(n):
    
    gc.collect()
    start = ticks_ms()
    
    #fade_out()
    #display.draw_image(f"/sd/background.raw", 0, 0, 240,320)
    
    backlight.duty_u16(16384)
    display.draw_image(f"/sd/nixie-{n}.raw", 0, 0, 240, 320)

    sleep(0.7)
    backlight.duty_u16(8192)
    next = ( n + 1 ) % 10

    # print(f"/sd/nixie-{n}-{next}.raw")
    # display.draw_image(f"/sd/nixie-{n}-{next}.raw", 0, 0, 240, 320)


    #print(f"/sd/nixie-{next}.raw")
    #display.draw_image(f"/sd/nixie-{next}.raw", 0, 0, 240, 320)
    #fade_in()
    print("Draw:", ticks_diff(ticks_ms(), start), "ms")

    


try:

    gc.collect()
    while True:
        for digit in range(10):
            print("free:", gc.mem_free())
            load_image(digit)
            count = 0
            
            # while count < 50:
            #     duty = random.randint(15000, 16384)
            #     backlight.duty_u16(duty)
            #     sleep(0.2)
            #     count += 1

            sleep(0.1)

except Exception as e:
    print("Error occurred:", e)

except KeyboardInterrupt:
    print("Program interrupted by the user")

finally:
    backlight.duty_u16(65535)

