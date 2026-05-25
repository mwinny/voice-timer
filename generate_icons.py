#!/usr/bin/env python3
"""Generate PWA icons for Voice Timer using only the Python stdlib.

Produces icon-180.png (Apple touch icon), icon-192.png and icon-512.png
(PWA manifest). Re-run after editing the colors / shape below.
"""
import struct
import zlib
from pathlib import Path

BG = (15, 17, 23)     # #0f1117 — matches app background
FG = (74, 222, 128)   # #4ade80 — accent green


def in_triangle(px, py, ax, ay, bx, by, cx, cy):
    def sign(x1, y1, x2, y2, x3, y3):
        return (x1 - x3) * (y2 - y3) - (x2 - x3) * (y1 - y3)
    d1 = sign(px, py, ax, ay, bx, by)
    d2 = sign(px, py, bx, by, cx, cy)
    d3 = sign(px, py, cx, cy, ax, ay)
    has_neg = d1 < 0 or d2 < 0 or d3 < 0
    has_pos = d1 > 0 or d2 > 0 or d3 > 0
    return not (has_neg and has_pos)


def make_pixels(size):
    ax, ay = size * 0.36, size * 0.26
    bx, by = size * 0.36, size * 0.74
    cx, cy = size * 0.74, size * 0.50
    raw = bytearray()
    for y in range(size):
        raw.append(0)  # PNG scanline filter: None
        for x in range(size):
            if in_triangle(x + 0.5, y + 0.5, ax, ay, bx, by, cx, cy):
                r, g, b = FG
            else:
                r, g, b = BG
            raw.extend((r, g, b))
    return bytes(raw)


def chunk(tag, data):
    crc = zlib.crc32(tag + data) & 0xFFFFFFFF
    return struct.pack('>I', len(data)) + tag + data + struct.pack('>I', crc)


def write_png(path, size):
    raw = make_pixels(size)
    sig = b'\x89PNG\r\n\x1a\n'
    ihdr = struct.pack('>IIBBBBB', size, size, 8, 2, 0, 0, 0)  # 8-bit RGB
    idat = zlib.compress(raw, 9)
    with open(path, 'wb') as f:
        f.write(sig + chunk(b'IHDR', ihdr) + chunk(b'IDAT', idat) + chunk(b'IEND', b''))


if __name__ == '__main__':
    out_dir = Path(__file__).parent
    for size in (180, 192, 512):
        target = out_dir / f'icon-{size}.png'
        write_png(target, size)
        print(f'wrote {target.name} ({size}x{size})')
