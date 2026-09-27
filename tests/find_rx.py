
from machine import Pin

p = Pin(4, Pin.IN, Pin.PULL_UP)

while True:
    print(p.value())
