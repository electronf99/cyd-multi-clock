# dfr0998.py
#
# MicroPython driver for sd3031 DFRobot DFR0998 Precision RTC
#
# Features:
#  - RTC date/time
#  - UNIX time helpers
#  - Temperature
#  - Battery voltage
#  - Alarms
#  - Countdown timer
#  - 32.768kHz output
#  - Programmable frequency output
#  - 70-byte battery-backed SRAM
#
# Tested against the DFRobot Arduino library register definitions.

import time


class DFR0998:

    I2C_ADDR = 0x32

    REG_SEC = 0x00
    REG_MIN = 0x01
    REG_HOUR = 0x02
    REG_WEEK = 0x03
    REG_DAY = 0x04
    REG_MONTH = 0x05
    REG_YEAR = 0x06

    REG_ALARM_SEC = 0x07
    REG_ALARM_MIN = 0x08
    REG_ALARM_HOUR = 0x09
    REG_ALARM_WEEK = 0x0A
    REG_ALARM_DAY = 0x0B
    REG_ALARM_MONTH = 0x0C
    REG_ALARM_YEAR = 0x0D
    REG_ALARM_CTRL = 0x0E

    REG_CTRL1 = 0x0F
    REG_CTRL2 = 0x10
    REG_CTRL3 = 0x11

    REG_COUNTDOWN = 0x13

    REG_TEMP = 0x16
    REG_IIC_CTRL = 0x17

    REG_BATTERY = 0x1A

    SRAM_START = 0x2C
    SRAM_END = 0x71
    SRAM_SIZE = 70

    # Week masks

    SUNDAY = 0x01
    MONDAY = 0x02
    TUESDAY = 0x04
    WEDNESDAY = 0x08
    THURSDAY = 0x10
    FRIDAY = 0x20
    SATURDAY = 0x40

    EVERY_DAY = 0x7F
    WORKDAYS = 0x3E

    # Frequency outputs

    FREQ_4096HZ = 2
    FREQ_1024HZ = 3
    FREQ_64HZ = 4
    FREQ_32HZ = 5
    FREQ_16HZ = 6
    FREQ_8HZ = 7
    FREQ_4HZ = 8
    FREQ_2HZ = 9
    FREQ_1HZ = 10

    FREQ_0_5HZ = 11
    FREQ_0_25HZ = 12
    FREQ_0_125HZ = 13
    FREQ_0_0625HZ = 14

    FREQ_1PPS = 15

    def __init__(self, i2c):
        self.i2c = i2c

        # Probe device
        self._read(self.REG_CTRL2, 1)

        # Same initialization used by DFRobot
        self._write(self.REG_IIC_CTRL, 0x80)

    # ---------------------------------------------------------
    # Utilities
    # ---------------------------------------------------------

    @staticmethod
    def _bcd_to_int(value):
        return value - 6 * (value >> 4)

    @staticmethod
    def _int_to_bcd(value):
        return value + 6 * (value // 10)

    def _read(self, reg, length=1):
        return self.i2c.readfrom_mem(
            self.I2C_ADDR,
            reg,
            length
        )

    def _raw_write(self, reg, data):
        self.i2c.writeto_mem(
            self.I2C_ADDR,
            reg,
            data
        )

    def _unlock_write(self):

        ctrl = self._read(self.REG_CTRL1, 2)

        ctrl1 = ctrl[0]
        ctrl2 = ctrl[1]

        self._raw_write(
            self.REG_CTRL2,
            bytes([(ctrl2 | 0x80) & 0xFF])
        )

        self._raw_write(
            self.REG_CTRL1,
            bytes([(ctrl1 | 0x84) & 0xFF])
        )

    def _lock_write(self):

        ctrl = self._read(self.REG_CTRL1, 2)

        ctrl1 = ctrl[0]
        ctrl2 = ctrl[1]

        self._raw_write(
            self.REG_CTRL1,
            bytes([ctrl1 & 0x7B])
        )

        self._raw_write(
            self.REG_CTRL2,
            bytes([ctrl2 & 0x7F])
        )

    def _write(self, reg, data):

        if isinstance(data, int):
            data = bytes([data])

        self._unlock_write()
        self._raw_write(reg, data)
        self._lock_write()

    # ---------------------------------------------------------
    # RTC
    # ---------------------------------------------------------

    def get_datetime(self):

        b = self._read(self.REG_SEC, 7)

        second = self._bcd_to_int(b[0] & 0x7F)
        minute = self._bcd_to_int(b[1] & 0x7F)

        hour_reg = b[2]

        if hour_reg & 0x80:
            hour = self._bcd_to_int(hour_reg & 0x7F)
        else:
            hour = self._bcd_to_int(hour_reg & 0x1F)

        weekday = self._bcd_to_int(b[3] & 0x07)

        day = self._bcd_to_int(b[4] & 0x3F)
        month = self._bcd_to_int(b[5] & 0x1F)
        year = 2000 + self._bcd_to_int(b[6])

        return (
            year,
            month,
            day,
            weekday,
            hour,
            minute,
            second
        )

    def set_datetime(
        self,
        year,
        month,
        day,
        hour,
        minute,
        second,
        weekday=0
    ):

        buf = bytes([
            self._int_to_bcd(second),
            self._int_to_bcd(minute),
            self._int_to_bcd(hour) | 0x80,
            self._int_to_bcd(weekday),
            self._int_to_bcd(day),
            self._int_to_bcd(month),
            self._int_to_bcd(year - 2000)
        ])

        self._write(self.REG_SEC, buf)

    def datetime(self, value=None):

        if value is None:
            return self.get_datetime()

        self.set_datetime(
            value[0],
            value[1],
            value[2],
            value[4],
            value[5],
            value[6],
            value[3]
        )

    def timestamp(self):

        y, m, d, _, hh, mm, ss = self.get_datetime()

        return (
            "{:04d}-{:02d}-{:02d} "
            "{:02d}:{:02d}:{:02d}"
        ).format(y, m, d, hh, mm, ss)

    def unix_time(self):

        y, m, d, _, hh, mm, ss = self.get_datetime()

        return int(
            time.mktime(
                (
                    y,
                    m,
                    d,
                    hh,
                    mm,
                    ss,
                    0,
                    0
                )
            )
        )

    def set_unix_time(self, unix_time):

        t = time.localtime(unix_time)

        self.set_datetime(
            t[0],
            t[1],
            t[2],
            t[3],
            t[4],
            t[5],
            t[6]
        )

    # ---------------------------------------------------------
    # Temperature
    # ---------------------------------------------------------

    def temperature(self):

        value = self._read(self.REG_TEMP, 1)[0]

        if value >= 128:
            value -= 256

        return value

    # ---------------------------------------------------------
    # Battery voltage
    # ---------------------------------------------------------

    def voltage(self):

        b = self._read(self.REG_BATTERY, 2)

        raw = (((b[0] & 0x80) >> 7) << 8) | b[1]

        return raw / 100.0

    # ---------------------------------------------------------
    # Alarm
    # ---------------------------------------------------------

    def set_date_alarm(
        self,
        year,
        month,
        day
    ):

        self._write(self.REG_CTRL3, 0x80)
        self._write(self.REG_CTRL2, 0x92)

        buf = bytes([
            0x00,
            0x00,
            0x00,
            0x00,
            self._int_to_bcd(day),
            self._int_to_bcd(month),
            self._int_to_bcd(year - 2000),
            0x70
        ])

        self._write(self.REG_ALARM_SEC, buf)

    def set_weekly_alarm(
        self,
        week_mask,
        hour,
        minute,
        second
    ):

        buf = bytes([
            self._int_to_bcd(second),
            self._int_to_bcd(minute),
            self._int_to_bcd(hour) | 0x80,
            week_mask,
            0x00,
            0x00,
            0x00,
            0x0F
        ])

        self._write(self.REG_CTRL3, 0x80)
        self._write(self.REG_CTRL2, 0x92)

        self._write(self.REG_ALARM_SEC, buf)

    def clear_alarm(self):

        # Arduino library simply reads CTRL1
        self._read(self.REG_CTRL1, 1)

    # ---------------------------------------------------------
    # Countdown timer
    # ---------------------------------------------------------

    def countdown(self, seconds):

        if seconds < 0:
            seconds = 0

        if seconds > 0xFFFFFF:
            seconds = 0xFFFFFF

        self._write(self.REG_CTRL2, 0x80)
        self._write(self.REG_CTRL2, 0xB4)
        self._write(self.REG_CTRL3, 0x20)

        self._write(
            self.REG_COUNTDOWN,
            bytes([
                seconds & 0xFF,
                (seconds >> 8) & 0xFF,
                (seconds >> 16) & 0xFF
            ])
        )

    # ---------------------------------------------------------
    # 32k output
    # ---------------------------------------------------------

    def enable_32k(self):

        reg = self._read(self.REG_CTRL3, 1)[0]
        reg &= ~0x40

        self._write(self.REG_CTRL3, reg)

    def disable_32k(self):

        reg = self._read(self.REG_CTRL3, 1)[0]
        reg |= 0x40

        self._write(self.REG_CTRL3, reg)

    # ---------------------------------------------------------
    # Frequency output
    # ---------------------------------------------------------

    def enable_frequency(self, freq):

        reg2 = self._read(self.REG_CTRL2, 1)[0]
        reg3 = self._read(self.REG_CTRL3, 1)[0]

        reg2 |= 0x21
        reg3 |= freq

        self._write(self.REG_CTRL2, reg2)
        self._write(self.REG_CTRL3, reg3)

    def disable_frequency(self):

        reg2 = self._read(self.REG_CTRL2, 1)[0]
        reg2 &= 0xFE

        self._write(self.REG_CTRL2, reg2)

    # ---------------------------------------------------------
    # SRAM
    # ---------------------------------------------------------

    def sram_write(self, offset, data):

        if isinstance(data, int):
            data = bytes([data])

        if offset < 0:
            raise ValueError("offset < 0")

        if offset + len(data) > self.SRAM_SIZE:
            raise ValueError("SRAM range exceeded")

        addr = self.SRAM_START + offset

        self._write(addr, data)

    def sram_read(self, offset, length=1):

        if offset < 0:
            raise ValueError("offset < 0")

        if offset + length > self.SRAM_SIZE:
            raise ValueError("SRAM range exceeded")

        addr = self.SRAM_START + offset

        return self._read(addr, length)

    def sram_clear(self, offset):

        self.sram_write(offset, b"\xFF")

    # ---------------------------------------------------------
    # Convenience string methods
    # ---------------------------------------------------------

    def write_string(self, offset, text):

        self.sram_write(
            offset,
            text.encode("utf-8")
        )

    def read_string(self, offset, length):

        return self.sram_read(
            offset,
            length
        ).decode("utf-8")

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    def is_present(self):
        try:
            self._read(self.REG_SEC, 1)
            return True
        except OSError:
            return False

    def __str__(self):
        return self.timestamp()
    
