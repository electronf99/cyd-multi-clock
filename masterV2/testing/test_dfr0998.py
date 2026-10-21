from machine import I2C, Pin
from dfr0998 import DFR0998
import time

i2c = I2C(
    0,
    scl=Pin(12),
    sda=Pin(11),
    freq=100_000
)

print("Connecting to updated DFR0998 Driver...")
rtc = DFR0998(i2c)
print("Device found and successfully initialized!")
rtc.set_datetime(2026,10,18,19,30,00,0 )
start_time = time.ticks_ms()

while True:
    elapsed_secs = time.ticks_diff(time.ticks_ms(), start_time) // 1000
    runtime = f"[{elapsed_secs // 3600:02d}:{(elapsed_secs % 3600) // 60:02d}:{elapsed_secs % 60:02d}]"

    try:
        current_time = rtc.timestamp()
        temp = rtc.temperature()
        vbat = rtc.voltage()
        print(f"{runtime} ONLINE -> Time: {current_time} | Temp: {temp}°C | Battery: {vbat}V")
    except OSError:
        print(f"\n{runtime} CRITICAL ERROR: Device dropped off bus.")
        break
        
    time.sleep(1.0)
