# Try using the font with the "Verovio" library


import pathlib
import venv
import os
import sys
import shutil
import xml.etree.ElementTree as ET


import subprocess
with open('s.py', 'w') as f_scr:
    f_scr.write('import fontforge\n')
    f_scr.write('fontforge.open("samuel-11.sfd").generate("samuel-12.svg")\n')
subprocess.run(['fontforge', '--script', 's.py'])



P = pathlib.Path(venv.sysconfig.get_path('platlib'))

if not P.joinpath('verovio').is_dir():
    print('Could not find verovio installed in this virtual environment. Try:\n\n    pip install verovio\n')
    sys.exit(-1)



if not os.access(P.joinpath('verovio'), os.W_OK):
    print('Do not have write access to the verovio installation. Most likely you are running\nfrom the main installation of python rather than a virtual environment.\nPlease call this script from a virtual environment. See:\n\n    https://docs.python.org/3/library/venv.html\n')
    sys.exit(-1)


# Put the font into the verovio data directory. For now, just copy one of the existing
# fonts and pretend it's ours.


__SRC__ = "Gootville"
__DST__ = "MyCompletelyNewFont"

Q = P.joinpath("verovio", "data")
shutil.rmtree(Q.joinpath(__DST__), ignore_errors=True)
shutil.copyfile(Q.joinpath(__SRC__ + ".xml"), Q.joinpath(__DST__ + ".xml"))
shutil.copytree(Q.joinpath(__SRC__), Q.joinpath(__DST__))



# Choose a specific glyph from the .SVG export

path_d_E050 = None

root = ET.parse('samuel-12.svg').getroot()
ns = {'xmlns': "http://www.w3.org/2000/svg"} 
glif = root.find("./xmlns:defs/xmlns:font/xmlns:glyph[@glyph-name='clefs.C']", ns)
if glif is not None:
    #print(glif.get('d'))
    path_d_E050 = glif.get('d')



if path_d_E050 is None:
    raise Exception

with open(Q.joinpath(__DST__, "E050.xml"), "w") as f_glif:
    f_glif.write('<symbol id="E050" viewBox="0 0 1000 1000" overflow="inherit"><path transform="scale(1,-1)" d="{0}"/></symbol>'.format(path_d_E050))




# Run Verovio to render the test score
import verovio

V = verovio.toolkit()
V.loadFile('test1.musicxml')
V.setFont(__DST__)   # use the font that we've just created
V.renderToSVGFile('test1out.svg')


# Change from SVG to PNG. There are surprisingly few cross-platform ways of doing this.
# Reportlab.graphics.renderPM gives terrible results - don't use it! This method using
# inkscape is okay, but it requires installing inkscape.



P_IN = pathlib.Path.cwd().resolve().joinpath("test1out.svg")
P_OUT = pathlib.Path.cwd().resolve().joinpath("test1out.png")

subprocess.run(['inkscape', '-o', str(P_OUT), '--export-overwrite', '--export-type=png', '--export-area={0}:{1}:{2}:{3}'.format(0, 0, 1000, 500), '--export-background=white', str(P_IN)])

