
# Rui Santos & Sara Santos - Random Nerd Tutorials
# Modified to fade the CYD backlight between image updates

from machine import Pin, SPI, PWM
from time import sleep, sleep_ms, ticks_ms, ticks_diff

from ili9341 import Display, color565
from xglcd_font import XglcdFont

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
    for duty in range(8192, 256, -32):
        backlight.duty_u16(duty)
        sleep_ms(2)
    
    backlight.duty_u16(256)
    sleep(0.01)

def fade_in():
    for duty in range(1024, 16384, 32):
        backlight.duty_u16(duty)
        sleep_ms(2)

    # Ensure full brightness
    #backlight.duty_u16(65535)


def load_image(n):
    fade_out()
    display.draw_image(f"nixie-{n}.raw", 0, 0, 240, 320)
    sleep(0.2)
    fade_in()


try:

    # # Timing tests
    # t0 = ticks_ms()
    # display.draw_image("nixie-0.raw", 0, 0, 240, 320)
    # print("draw:", ticks_diff(ticks_ms(), t0), "ms")

    # # Warm cache
    # display.draw_image("nixie-0.raw", 0, 0, 240, 320)

    # t0 = ticks_ms()
    # display.draw_image("nixie-0.raw", 0, 0, 240, 320)
    # print("draw:", ticks_diff(ticks_ms(), t0), "ms")



    # Main loop
    while True:
        for digit in range(10):
            load_image(digit)
            sleep(5)

except Exception as e:
    print("Error occurred:", e)

except KeyboardInterrupt:
    print("Program interrupted by the user")

finally:
    backlight.duty_u16(65535)


# # Rui Santos & Sara Santos - Random Nerd Tutorials
# # Complete project details at https://RandomNerdTutorials.com/micropython-cheap-yellow-display-board-cyd-esp32-2432s028r/
 
# from machine import Pin, SPI, ADC, idle
# import os
# from time import sleep



# # Save this file as ili9341.py https://github.com/rdagger/micropython-ili9341/blob/master/ili9341.py
# from ili9341 import Display, color565
# # Save this file as xglcd_font.py https://github.com/rdagger/micropython-ili9341/blob/master/xglcd_font.py
# from xglcd_font import XglcdFont

# # Function to set up SPI for TFT display
# display_spi = SPI(1, baudrate=80000000, sck=Pin(14), mosi=Pin(13))
# # Set up display
# display = Display(display_spi, dc=Pin(2), cs=Pin(15), 
#                   rst=Pin(15), width=240, height=320, rotation=270)

# print('Display height: ' + str(display.height))
# print('Display width: ' + str(display.width))

# # Set colors (foreground) and background color
# white_color = color565(255, 255, 255)  # white
# black_color = color565(0, 0, 0)  # Black

# # Turn on display backlight
# backlight = Pin(21, Pin.OUT)
# backlight.on()

# # Clear display
# #display.clear(black_color)

# def load_image(n):
#     display.draw_image(f"nixie-{n}.raw", 0, 0, 240, 320)

# try:

#     from time import ticks_ms, ticks_diff

#     t0 = ticks_ms()
#     display.draw_image("nixie-0.raw", 0, 0, 240, 320)
#     print("draw:", ticks_diff(ticks_ms(), t0), "ms")



#     # warm cache
#     display.draw_image("nixie-0.raw", 0, 0, 240, 320)

#     t0 = ticks_ms()
#     display.draw_image("nixie-0.raw", 0, 0, 240, 320)
#     print("draw:", ticks_diff(ticks_ms(), t0), "ms")


#     t0 = ticks_ms()

#     with open("nixie-0.raw", "rb") as f:
#         while f.read(4096):
#             pass

#     print("read:", ticks_diff(ticks_ms(), t0), "ms")



#     while True:
#         n=0
#         for digit in range(10):
#             load_image(digit)
#             #sleep(1)

# except Exception as e:
#     print('Error occured: ', e)
# except KeyboardInterrupt:
#     print('Program Interrupted by the user')