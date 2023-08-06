import datetime
import math
import struct


def string_to_raw(s: str) -> bytes:
    return bytes(s, 'utf8')


def float_to_raw(f: float) -> bytes:
    return struct.pack('<d', f)


def time_to_raw(t: datetime.datetime) -> bytes:
    bts = bytearray(15)
    bts[0] = 1

    offset = 62135596800

    sec = int(math.floor(t.timestamp()))
    fracSec = t.timestamp() - sec

    sec += offset
    for i in range(8):
        bts[8 - i] = sec % 256
        sec //= 256

    nsec = int(fracSec * 1e9)
    for i in range(4):
        bts[12 - i] = nsec % 256
        nsec //= 256

    return bytes(bts)
