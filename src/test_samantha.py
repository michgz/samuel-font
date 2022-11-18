# Try using the font with the "Verovio" library


import pathlib
import venv
import os
import sys
import shutil
import textwrap
import xml.etree.ElementTree as ET
import subprocess
from build_font import build_font


__NAME__ = "Samantha"


Compare_Image = "0102=95.jpg"


def CreateVerovioFont(src, name, dstdir):
    # src is a fontforge font. dstdir is a directory to put the Verovio-compatible
    # font data to.
    
    __TMP__ = "samuel-13"   # name of temporary SVG fontforge file to create. For now,
                             # it can just go in the working directory.
    
    
    # Make sure the destination directory is a pathlib path.
    if not isinstance(dstdir, pathlib.Path):
        dstdir = pathlib.Path(dstdir)
    
    with open('s5.py', 'w') as f_scr:
        f_scr.write('import fontforge\n')
        f_scr.write('fontforge.open("{0}").generate("{1}.svg")\n'.format(src, __TMP__))
    subprocess.run(['fontforge', '--script', 's5.py'])



    __DST__ = name

    shutil.rmtree(dstdir.joinpath(__DST__), ignore_errors=True)
    os.mkdir(dstdir.joinpath(__DST__))


    root = ET.parse('{0}.svg'.format(__TMP__)).getroot()
    ns = {'xmlns': "http://www.w3.org/2000/svg"} 

    ALL = []



    with open('s4.py', 'w') as f_scr:
        f_scr.write(textwrap.dedent("""
          import fontforge
          __DST__ = "{0}"
          __NAME__ = "{1}"
          f = fontforge.open("{2}")
          """.format(__DST__, name, str(src)) + """
          with open(__DST__ + ".xml", "w") as f2:
              f2.write('<?xml version="1.0" encoding="UTF-8"?>\\n<bounding-boxes font-family="{0}" units-per-em="1000">\\n'.format(__NAME__))
              for GLIF in f.glyphs():
                  (xa, ya, xb, yb) = GLIF.boundingBox()
                  xah = GLIF.width    # Assume h-a-x means advance width
                  f2.write('  <g c="{0:04X}" x="{2:0.1f}" y="{3:0.1f}" w="{4:0.1f}" h="{5:0.1f}" h-a-x="{6:0.1f}" n="{1}"'.format(GLIF.unicode, GLIF.glyphname, xa, ya, xb-xa, yb-ya, xah))
                  if len(GLIF.anchorPoints) == 0:
                      f2.write('/>\\n')
                  else:
                      f2.write('>\\n')
                      for ANCHOR in GLIF.anchorPoints:
                          f2.write('    <a n="{0}" x="{2:0.1f}" y="{3:0.1f}"/>\\n'.format(ANCHOR[0], ANCHOR[1], ANCHOR[2]/250.0, ANCHOR[3]/250.0))
                      f2.write('  </g>\\n')
              f2.write('</bounding-boxes>\\n')
          """))
    subprocess.run(['fontforge', '--script', 's4.py'])
    shutil.copy( __DST__ + ".xml", dstdir.joinpath(__DST__ + ".xml"))



    for glif in root.findall("./xmlns:defs/xmlns:font/xmlns:glyph", ns):

        path_d = None

        if glif is not None:
            #print(glif.get('d'))
            path_d = glif.get('d')
            uni_str = glif.get('unicode')
            if len(uni_str) == 8 and uni_str.startswith("&#x") and uni_str.endswith(";"):
                uni_val = uni_str[3:7].upper()
            elif len(uni_str) == 1:
                uni_val = "{0:04X}".format(ord(uni_str[0]))
            else:
                try:
                    uni_val = "{0:04X}".format(int(uni_str))
                except:
                    raise Exception
            glif_name = glif.get('glyph-name')


            if path_d is None:
                raise Exception("Missing glyph: {0}".format(EE[0]))

            with open(dstdir.joinpath(__DST__, uni_val + ".xml"), "w") as f_glif:
                f_glif.write('<symbol id="{0}" viewBox="0 0 1000 1000" overflow="inherit"><path transform="scale(1,-1)" d="{1}"/></symbol>'.format(uni_val, path_d))

            ALL.append({'file': uni_val, 'name': glif_name})






def test_verovio(in_path):

    
    P = pathlib.Path(__file__).parent.joinpath("verovio_data")
    P.mkdir(exist_ok =True)

    CreateVerovioFont(in_path, __NAME__, P)


    # Copy the fonts from the verovio directory
    Q = pathlib.Path(venv.sysconfig.get_path('platlib'))

    if not Q.joinpath('verovio').is_dir():
        print('Could not find verovio installed in this virtual environment. Try:\n\n    pip install verovio\n')
        sys.exit(-1)

    shutil.copy(Q.joinpath("verovio", "data", "Bravura.xml"), P)
    shutil.copytree(Q.joinpath("verovio", "data", "Bravura"), P.joinpath("Bravura"), dirs_exist_ok=True)
    shutil.copy(Q.joinpath("verovio", "data", "Leipzig.xml"), P)
    shutil.copytree(Q.joinpath("verovio", "data", "Leipzig"), P.joinpath("Leipzig"), dirs_exist_ok=True)
    shutil.copytree(Q.joinpath("verovio", "data", "text"), P.joinpath("text"), dirs_exist_ok=True)


    # Run Verovio to render the test score
    import verovio

    V = verovio.toolkit()
    V.setResourcePath(str(P))
    V.loadFile('test4.musicxml')
    V.setFont(__NAME__)   # use the font that we've just created
    V.renderToSVGFile('test4out.svg')





    # Change from SVG to PNG. There are surprisingly few cross-platform ways of doing this.
    # Reportlab.graphics.renderPM gives terrible results - don't use it! This method using
    # inkscape is okay, but it requires installing inkscape.



    P_IN = pathlib.Path.cwd().resolve().joinpath("test4out.svg")
    P_OUT = pathlib.Path.cwd().resolve().joinpath("test4out.png")

    subprocess.run(['inkscape', '-o', str(P_OUT), '--export-overwrite', '--export-type=png', '--export-area={0}:{1}:{2}:{3}'.format(0, 0, 1750, 900), '--export-background=#FAE9C4', str(P_IN)])


if __name__=="__main__":
    if len(sys.argv) < 2:
        sys.exit(-1)
    test_verovio(pathlib.Path(sys.argv[1]))

