
# Do a test with the python PIL/Pillow library.

import pathlib
import struct
import sys


from PIL import Image, ImageDraw, ImageFont

def test_pillow(in_otf):

    TEST_CLEFS = False
    TEST_FLAGS = False
    TEST_DYNAMICS = True
    


    if TEST_CLEFS:
        # Show clefs and different magnifications
        II = Image.new("L", (600, 500), 255)
        DD = ImageDraw.Draw(II)
        for I, size in enumerate([20, 30, 44, 64, 100, 196]):
            font = ImageFont.truetype(str(in_otf), size=size)
            DD.text((20 + 70*I, 40), u"\uF400", font=font)
            DD.text((20 + 70*I, 240), u"\uF401", font=font)
            
        II.show()

    if TEST_FLAGS:
        # Check all up- and down- flags
        II = Image.new("L", (600, 500), 255)
        DD = ImageDraw.Draw(II)
        font = ImageFont.truetype(str(in_otf), size=64)
        for I, Uni in enumerate(range(0xE240, 0xE250, 2)):   # Up flags
            DD.text((20 + 70*I, 140), struct.pack("<H", Uni).decode('UTF-16LE'), font=font)
        for I, Uni in enumerate(range(0xE241, 0xE250, 2)):   # Down flags
            DD.text((20 + 70*I, 240), struct.pack("<H", Uni).decode('UTF-16LE'), font=font)

        II.show()

    if TEST_DYNAMICS:
        # Check the kerning on dynamic markings
        II = Image.new("L", (600, 800), 255)
        DD = ImageDraw.Draw(II)
        font = ImageFont.truetype(str(in_otf), size=196)
        for I, UU in enumerate([0xE520, 0xE522, 0xE521]):
            DD.text((50 + 90*I, 40), struct.pack("<H", UU).decode('UTF-16LE'), font=font)
        
        SPACINGS = [0, 40, 100, 180, 280, 380, 480, 580]
        
        font = ImageFont.truetype(str(in_otf), size=64)
        PIANISSIMO = [(1, 0xE520), (2, 0xE52B), (3, 0xE52A), (4, 0xE529), (5, 0xE528), (6, 0xE527)]
        for I, UU in enumerate(PIANISSIMO):
            DD.text((30 + SPACINGS[I], 240), u'\uE520' * UU[0], font=font)
            DD.text((30 + SPACINGS[I], 340), struct.pack("<H", UU[1]).decode('UTF-16LE'), font=font)

        FORTISSIMO = [(1, 0xE522), (2, 0xE52F), (3, 0xE530), (4, 0xE531), (5, 0xE532), (6, 0xE533)]
        for I, UU in enumerate(FORTISSIMO):
            DD.text((30 + SPACINGS[I], 440), u'\uE522' * UU[0], font=font)
            DD.text((30 + SPACINGS[I], 540), struct.pack("<H", UU[1]).decode('UTF-16LE'), font=font)
            
        MIXED = [(u'\uE522\uE520', 0xE534), (u'\uE520\uE522', 0xE52E)]
        for I, UU in enumerate(MIXED):
            DD.text((30 + 60*I, 640), UU[0], font=font)
            DD.text((30 + 60*I, 740), struct.pack("<H", UU[1]).decode('UTF-16LE'), font=font)

            
        II.show()
        


if __name__=="__main__":
    if len(sys.argv) < 2:
        sys.exit(-1)
    test_pillow(pathlib.Path(sys.argv[1]))

