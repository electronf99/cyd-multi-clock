# Save this file on your board as tsl2591.py
from machine import I2C
import time

class TSL2591:
    def __init__(self, i2c, address=0x29):
        self.i2c = i2c
        self.address = address
        
        # Verify device ID (Should return 0x50)
        if self._read_reg(0x12) != 0x50:
            raise RuntimeError("TSL2591 not found on I2C bus!")
            
        # Enable device (Power on and ALS enable)
        self._write_reg(0x00, 0x01 | 0x02 | 0x80) 
        
        # Set default timing (100ms) and gain (Low / 1x)
        self.set_timing_gain(0x00, 0x00)

    def _write_reg(self, reg, val):
        self.i2c.writeto_mem(self.address, 0xA0 | reg, bytes([val]))

    def _read_reg(self, reg):
        return self.i2c.readfrom_mem(self.address, 0xA0 | reg, 1)[0]

    def set_timing_gain(self, integration_time=0x00, gain=0x00):
        # integration_time: 0x00=100ms, 0x01=200ms, 0x02=300ms
        # gain: 0x00=Low, 0x10=Med, 0x20=High
        self._write_reg(0x01, integration_time | gain)

    def read_raw(self):
        # Read channels 0 and 1 (Full spectrum and IR)
        data = self.i2c.readfrom_mem(self.address, 0xA0 | 0x14, 4)
        full = data[1] << 8 | data[0]
        ir = data[3] << 8 | data[2]
        return full, ir

    def read_lux(self):
        full, ir = self.read_raw()
        
        # 1. Handle sensor saturation or total darkness safety checks
        if full == 0xFFFF or full == 0:
            return 0.0  
            
        # Basic Lux calculation formula
        atime = 100.0
        again = 1.0
        cpl = (atime * again) / 408.0
        lux = (full - ir) * (1.0 - (ir / full)) / cpl
        return max(lux, 0.0)