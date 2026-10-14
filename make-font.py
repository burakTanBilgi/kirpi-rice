#!/usr/bin/env python3
# make-font.py: adds the two half blocks (▀ ▄) to Debian's Terminus Bold 32x16 console font,
# which has only the full block. They take the places of ¶ and §, which the rest screen never uses.
#   usage: make-font.py Lat15-TerminusBold32x16.psf.gz kirpi-32x16.psf.gz
import gzip, struct, sys
src, out = sys.argv[1], sys.argv[2]
d = gzip.open(src).read()
magic, ver, hs, flags, num, cs, h, w = struct.unpack('<IIIIIIII', d[:32])
assert magic == 0x864ab572 and flags & 1, 'not a PSF2 font with a unicode table'
rowb = cs // h
glyphs = [bytearray(d[hs + i*cs: hs + (i+1)*cs]) for i in range(num)]
table = d[hs + num*cs:].split(b'\xff')[:num]
full = b'\xff' * rowb; none = b'\x00' * rowb
def slot(ch):
    for i, e in enumerate(table):
        if ch.encode() in e: return i
    sys.exit(f'no glyph for {ch} to replace')
for ch, old, top in (('▀', '¶', True), ('▄', '§', False)):
    i = slot(old)
    glyphs[i] = bytearray(b''.join(full if (r < h//2) == top else none for r in range(h)))
    table[i] = ch.encode()
body = d[:hs] + b''.join(glyphs) + b''.join(e + b'\xff' for e in table)
gzip.open(out, 'wb').write(body)
t = body[hs + num*cs:].decode('utf-8', 'replace')
print(out, num, 'glyphs', f'{w}x{h}', {c: c in t for c in '▀▄█·'})
