
# Do a test with the python PIL/Pillow library.

import pathlib
import sys


from PIL import Image, ImageDraw, ImageFont

def test_pillow(in_otf):

    II = Image.new("L", (600, 500), 255)
    DD = ImageDraw.Draw(II)
    for I, size in enumerate([20, 30, 44, 64, 100, 196]):
        font = ImageFont.truetype(str(in_otf), size=size)
        DD.text((20 + 70*I, 40), u"\uF400", font=font)
        DD.text((20 + 70*I, 240), u"\uF401", font=font)
        
    II.show()


if __name__=="__main__":
    if len(sys.argv) < 2:
        sys.exit(-1)
    test_pillow(pathlib.Path(sys.argv[1]))

