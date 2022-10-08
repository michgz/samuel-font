
# Do a test with the python PIL/Pillow library.

import pathlib
import struct
import sys


from PIL import Image, ImageDraw, ImageFont

def test_pillow(in_otf):

    TEST_CLEFS = False
    TEST_FLAGS = True


    if TEST_CLEFS:
        II = Image.new("L", (600, 500), 255)
        DD = ImageDraw.Draw(II)
        for I, size in enumerate([20, 30, 44, 64, 100, 196]):
            font = ImageFont.truetype(str(in_otf), size=size)
            DD.text((20 + 70*I, 40), u"\uF400", font=font)
            DD.text((20 + 70*I, 240), u"\uF401", font=font)
            
        II.show()

    if TEST_FLAGS:
        II = Image.new("L", (600, 500), 255)
        DD = ImageDraw.Draw(II)
        font = ImageFont.truetype(str(in_otf), size=64)
        for I, Uni in enumerate(range(0xE240, 0xE250, 2)):   # Up flags
            DD.text((20 + 70*I, 40), struct.pack("<H", Uni).decode('UTF-16LE'), font=font)
        for I, Uni in enumerate(range(0xE241, 0xE250, 2)):   # Down flags
            DD.text((20 + 70*I, 240), struct.pack("<H", Uni).decode('UTF-16LE'), font=font)

        II.show()

if __name__=="__main__":
    if len(sys.argv) < 2:
        sys.exit(-1)
    test_pillow(pathlib.Path(sys.argv[1]))

