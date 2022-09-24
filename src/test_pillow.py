
# Do a test with the python PIL/Pillow library.

from PIL import Image, ImageDraw, ImageFont

font = ImageFont.truetype("_build/otf/samuel-14.otf", size=20)


II = Image.new("L", (100, 100), 255)
ImageDraw.Draw(II).text((10,10), u"\uE050", font=font)
II.show()
