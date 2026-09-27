
from machine import SDCard
import os

sd = SDCard(
    slot=2,
    sck=18,
    miso=19,
    mosi=23,
    cs=5
)

os.mount(sd, "/sd")

print(os.listdir("/sd"))
