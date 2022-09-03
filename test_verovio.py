# Try using the font with the "Verovio" library


import pathlib
import venv
import os
import sys
import shutil
import xml.etree.ElementTree as ET
import subprocess


DEFAULTS= {"staffLineThickness": 19, "stemThickness": 20, "stemHeight": 1000, "flags": {"h": 80, "w": 180, "drop": 70, "sep": 40}}


S = "DEFAULTS = {0}".format(str(DEFAULTS)) +  """
import fontforge
F = fontforge.open("samuel-11.sfd")
for X in F.glyphs():
    #print(X)
    #print(dir(X))
    #print(X.glyphname)
    if X.glyphname == "uniE0A4":
        print(X.anchorPoints)

# 5-line stave. Included in "sebastian"
C = F.createChar(0x003D, "equal")
pen = C.glyphPen()
for YC in [7, 260, 513, 768, 1021]:
    pen.moveTo((998,YC-DEFAULTS["staffLineThickness"]))
    pen.lineTo((0,YC-DEFAULTS["staffLineThickness"]))
    pen.lineTo((0,YC))
    pen.lineTo((998,YC))
    pen.closePath()
pen = None

# Stem. Not in any example fonts
C = F.createChar(0xE210, "uniE210")
pen = C.glyphPen()
pen.moveTo((0,0))
pen.lineTo((DEFAULTS["stemThickness"],0))
pen.lineTo((DEFAULTS["stemThickness"],DEFAULTS["stemHeight"]))
pen.lineTo((0,1000))
pen.closePath()
pen = None




X, Y = None, None
for A in F['uniE0A4'].anchorPoints:
    if A[0] == 'stemUpSE' and A[1] == 'base':
        X, Y = A[2], A[3]


# Now do all the up flags
FLAGS_UP = [
    ("flag8thUp", 1, "E240"),
    ("flag16thUp", 2, "E242"),
    ("flag32ndUp", 3, "E244"),
    ("flag64thUp", 4, "E246"),
    ("flag128thUp", 5, "E248"),
    ("flag256thUp", 6, "E24A"),
    ("flag512thUp", 7, "E24C"),
    ("flag1024thUp", 8, "E24E")]


for _, flag_count, uni in FLAGS_UP:

    C = F.createChar(int(uni, 16), "uni" + uni)
    pen = C.glyphPen()
    
    # Quavers and semiquavers use the standard stem height. After that, need to
    # start extending.
    if flag_count == 1:
        flag_base = 0
    else:
        flag_base = -1

    for J in range(flag_count):
        pen.moveTo((X-DEFAULTS["stemThickness"],                          Y+DEFAULTS["stemHeight"]+(DEFAULTS["flags"]["h"]+DEFAULTS["flags"]["sep"])*(J+flag_base)   ))
        pen.lineTo((X-DEFAULTS["stemThickness"]+DEFAULTS["flags"]["w"],   Y+DEFAULTS["stemHeight"]+(DEFAULTS["flags"]["h"]+DEFAULTS["flags"]["sep"])*(J+flag_base)-DEFAULTS["flags"]["drop"]   ))
        pen.lineTo((X-DEFAULTS["stemThickness"]+DEFAULTS["flags"]["w"],   Y+DEFAULTS["stemHeight"]+(DEFAULTS["flags"]["h"]+DEFAULTS["flags"]["sep"])*(J+flag_base)-DEFAULTS["flags"]["drop"]-DEFAULTS["flags"]["h"]   ))
        pen.lineTo((X-DEFAULTS["stemThickness"],                          Y+DEFAULTS["stemHeight"]+(DEFAULTS["flags"]["h"]+DEFAULTS["flags"]["sep"])*(J+flag_base)-DEFAULTS["flags"]["h"]   ))
        pen.closePath()

    # Draw a partial stem between the mid-points of the extreme flags
    if flag_count >= 2:
        pen.moveTo((X-DEFAULTS["stemThickness"],                          Y+DEFAULTS["stemHeight"]+(DEFAULTS["flags"]["h"]+DEFAULTS["flags"]["sep"])*(flag_base+flag_count-1)-DEFAULTS["flags"]["h"]*0.5   ))
        pen.lineTo((X                          ,                          Y+DEFAULTS["stemHeight"]+(DEFAULTS["flags"]["h"]+DEFAULTS["flags"]["sep"])*(flag_base+flag_count-1)-DEFAULTS["flags"]["h"]*0.5   ))
        pen.lineTo((X                          ,                          Y+DEFAULTS["stemHeight"]+(DEFAULTS["flags"]["h"]+DEFAULTS["flags"]["sep"])*(flag_base-1)           +DEFAULTS["flags"]["h"]*0.5   ))
        pen.lineTo((X-DEFAULTS["stemThickness"],                          Y+DEFAULTS["stemHeight"]+(DEFAULTS["flags"]["h"]+DEFAULTS["flags"]["sep"])*(flag_base-1)           +DEFAULTS["flags"]["h"]*0.5   ))
        pen.closePath()

        C.removeOverlap()
    pen = None
    

NOTES_UP = [
    ("noteQuarterUp", "E1D5",  None),
    ("note8thUp", "E1D7",  "E240"),
    ("note16thUp", "E1D9",  "E242"),
    ("note32ndUp", "E1DB",  "E244"),
    ("note64thUp", "E1DD",  "E246"),
    ("note128thUp", "E1DF",  "E248"),
    ("note256thUp", "E1E1",  "E24A"),
    ("note512thUp", "E1E3",  "E24C"),
    ("note1024thUp", "E1E5",  "E24E")]

    
for _, uni, uni_flag in NOTES_UP:

    # Notehead with stem up
    C = F.createChar(int(uni, 16), "uni" + uni)
    pen = C.glyphPen()
    F['uniE0A4'].draw(pen)
    if uni_flag:
        try:
            F['uni' + uni_flag].draw(pen)       
        except TypeError:
          print('uni' + uni_flag)
    pen.moveTo((X,Y))
    pen.lineTo((X-DEFAULTS["stemThickness"],Y))
    pen.lineTo((X-DEFAULTS["stemThickness"],Y+DEFAULTS["stemHeight"]))
    pen.lineTo((X,Y+DEFAULTS["stemHeight"]))
    pen.closePath()
    C.removeOverlap()
    pen = None





X, Y = None, None
for A in F['uniE0A4'].anchorPoints:
    if A[0] == 'stemDownNW' and A[1] == 'base':
        X, Y = A[2], A[3]
        
        

# Now do all the down flags
FLAGS_DOWN = [
    ("flag8thDown", 1, "E241"),
    ("flag16thDown", 2, "E243"),
    ("flag32ndDown", 3, "E245"),
    ("flag64thDown", 4, "E247"),
    ("flag128thDown", 5, "E249"),
    ("flag256thDown", 6, "E24B"),
    ("flag512thDown", 7, "E24D"),
    ("flag1024thDown", 8, "E24F")]


for _, flag_count, uni in FLAGS_DOWN:

    C = F.createChar(int(uni, 16), "uni" + uni)
    pen = C.glyphPen()
    
    # Quavers and semiquavers use the standard stem height. After that, need to
    # start extending.
    if flag_count == 1:
        flag_base = 0
    else:
        flag_base = 1

    for J in range(flag_count):
        pen.moveTo((X,                          Y-DEFAULTS["stemHeight"]+(DEFAULTS["flags"]["h"]+DEFAULTS["flags"]["sep"])*(-J+flag_base)                            +DEFAULTS["flags"]["h"]))
        pen.lineTo((X+DEFAULTS["flags"]["w"],   Y-DEFAULTS["stemHeight"]+(DEFAULTS["flags"]["h"]+DEFAULTS["flags"]["sep"])*(-J+flag_base)+DEFAULTS["flags"]["drop"]  +DEFAULTS["flags"]["h"]   ))
        pen.lineTo((X+DEFAULTS["flags"]["w"],   Y-DEFAULTS["stemHeight"]+(DEFAULTS["flags"]["h"]+DEFAULTS["flags"]["sep"])*(-J+flag_base)+DEFAULTS["flags"]["drop"]  ))
        pen.lineTo((X,                          Y-DEFAULTS["stemHeight"]+(DEFAULTS["flags"]["h"]+DEFAULTS["flags"]["sep"])*(-J+flag_base)   ))
        pen.closePath()


    # Draw a partial stem between the mid-points of the extreme flags
    if flag_count >= 2:
        pen.moveTo((X                          ,                          Y-DEFAULTS["stemHeight"]+(DEFAULTS["flags"]["h"]+DEFAULTS["flags"]["sep"])*(flag_base)             +0.5*DEFAULTS["flags"]["h"]   ))
        pen.lineTo((X+DEFAULTS["stemThickness"],                          Y-DEFAULTS["stemHeight"]+(DEFAULTS["flags"]["h"]+DEFAULTS["flags"]["sep"])*(flag_base)             +0.5*DEFAULTS["flags"]["h"]   ))
        pen.lineTo((X+DEFAULTS["stemThickness"],                          Y-DEFAULTS["stemHeight"]+(DEFAULTS["flags"]["h"]+DEFAULTS["flags"]["sep"])*(flag_base-flag_count+2)-0.5*DEFAULTS["flags"]["h"]   ))
        pen.lineTo((X                          ,                          Y-DEFAULTS["stemHeight"]+(DEFAULTS["flags"]["h"]+DEFAULTS["flags"]["sep"])*(flag_base-flag_count+2)-0.5*DEFAULTS["flags"]["h"]   ))
        pen.closePath()
        
        C.removeOverlap()
    pen = None


NOTES_DOWN = [
    ("noteQuarterDown", "E1D6",  None),
    ("note8thDown", "E1D8",  "E241"),
    ("note16thDown", "E1DA",  "E243"),
    ("note32ndDown", "E1DC",  "E245"),
    ("note64thDown", "E1DE",  "E247"),
    ("note128thDown", "E1E0",  "E249"),
    ("note256thDown", "E1E2",  "E24B"),
    ("note512thDown", "E1E4",  "E24D"),
    ("note1024thDown", "E1E6",  "E24F")]

    
for _, uni, uni_flag in NOTES_DOWN:

    # Notehead with stem down
    C = F.createChar(int(uni, 16), "uni" + uni)
    pen = C.glyphPen()
    F['uniE0A4'].draw(pen)
    if uni_flag:
        F['uni' + uni_flag].draw(pen)       
    pen.moveTo((X,Y))
    pen.lineTo((X+DEFAULTS["stemThickness"],Y))
    pen.lineTo((X+DEFAULTS["stemThickness"],Y-DEFAULTS["stemHeight"]))
    pen.lineTo((X,Y-DEFAULTS["stemHeight"]))
    pen.closePath()
    C.removeOverlap()
    pen = None
      




F.save("samuel-12.sfd")
"""


with open('s2.py', 'w') as f_scr:
    f_scr.write(S)
subprocess.run(['fontforge', '--script', 's2.py'])

sys.exit(0)



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


__SRC__ = "Bravura"
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

