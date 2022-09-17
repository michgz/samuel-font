# Try using the font with the "Verovio" library


import pathlib
import venv
import os
import sys
import shutil
import textwrap
import xml.etree.ElementTree as ET
import subprocess


__NAME__ = "Samuel"
__VERSION__ = "0.0.1"

DEFAULTS= {"staffLineThickness": 19, "stemThickness": 20, "stemHeight": 1000,   \
              "flags": {"h": 80, "w": 180, "drop": 70, "sep": 40},    \
              "sharp":   {"h": 540, "w": 110, "hthick": 20, "vthick": 80, "hsep": 60, "vsep": 200, "vdrop": 50},  \
              "natural": {"h": 540,           "hthick": 20, "vthick": 80, "hsep": 60, "vsep": 200, "vdrop": 50},  \
              "barlines": {"hthick1": 10, "hthick2": 60, "hsep": 20, "hsep_dots": 20, "repeat_diameter": 30},   \
              "restLonga": {"w": 210},   \
              "rest": {"w": 368, "h": 125},    \
          }


S = "DEFAULTS = {0}".format(str(DEFAULTS)) +  """
import fontforge
import json
import pathlib

with open(pathlib.Path("metadata", "glyphnames.json"), "r") as fnames:
    names = json.load(fnames)

def GlyphName(u):
    X = [x for x in names if names[x]['codepoint'] == "U+{0:04X}".format(u)]
    if len(X) != 1:
        raise Exception(u)
    return X[0]

F = fontforge.open("samuel-11.sfdir")

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


# whole note -- is just a whole notehead with no stems

C = F.createChar(0xE1D2, GlyphName(0xE1D2))
pen = C.glyphPen()
F[GlyphName(0xE0A2)].draw(pen)
pen = None


# Stem. Not in any example fonts
C = F.createChar(0xE210, GlyphName(0xE210))
pen = C.glyphPen()
pen.moveTo((0,0))
pen.lineTo((DEFAULTS["stemThickness"],0))
pen.lineTo((DEFAULTS["stemThickness"],DEFAULTS["stemHeight"]))
pen.lineTo((0,1000))
pen.closePath()
pen = None




# Barlines

C = F.createChar(0xE030, GlyphName(0xE030))
pen = C.glyphPen()
pen.moveTo((0,0))
pen.lineTo((0,1000))
pen.lineTo((DEFAULTS["barlines"]["hthick1"],1000))
pen.lineTo((DEFAULTS["barlines"]["hthick1"],0))
pen.closePath()
pen = None

C = F.createChar(0xE031, GlyphName(0xE031))
pen = C.glyphPen()
X = 0
pen.moveTo((X+0,0))
pen.lineTo((X+0,1000))
pen.lineTo((X+DEFAULTS["barlines"]["hthick1"],1000))
pen.lineTo((X+DEFAULTS["barlines"]["hthick1"],0))
pen.closePath()
X = DEFAULTS["barlines"]["hthick1"] + DEFAULTS["barlines"]["hsep"]
pen.moveTo((X+0,0))
pen.lineTo((X+0,1000))
pen.lineTo((X+DEFAULTS["barlines"]["hthick1"],1000))
pen.lineTo((X+DEFAULTS["barlines"]["hthick1"],0))
pen.closePath()
pen = None

C = F.createChar(0xE032, GlyphName(0xE032))
pen = C.glyphPen()
X = 0
pen.moveTo((X+0,0))
pen.lineTo((X+0,1000))
pen.lineTo((X+DEFAULTS["barlines"]["hthick1"],1000))
pen.lineTo((X+DEFAULTS["barlines"]["hthick1"],0))
pen.closePath()
X = DEFAULTS["barlines"]["hthick1"] + DEFAULTS["barlines"]["hsep"]
pen.moveTo((X+0,0))
pen.lineTo((X+0,1000))
pen.lineTo((X+DEFAULTS["barlines"]["hthick2"],1000))
pen.lineTo((X+DEFAULTS["barlines"]["hthick2"],0))
pen.closePath()
pen = None

C = F.createChar(0xE033, GlyphName(0xE033))
pen = C.glyphPen()
X = 0
pen.moveTo((X+0,0))
pen.lineTo((X+0,1000))
pen.lineTo((X+DEFAULTS["barlines"]["hthick2"],1000))
pen.lineTo((X+DEFAULTS["barlines"]["hthick2"],0))
pen.closePath()
X = DEFAULTS["barlines"]["hthick2"] + DEFAULTS["barlines"]["hsep"]
pen.moveTo((X+0,0))
pen.lineTo((X+0,1000))
pen.lineTo((X+DEFAULTS["barlines"]["hthick1"],1000))
pen.lineTo((X+DEFAULTS["barlines"]["hthick1"],0))
pen.closePath()
pen = None

C = F.createChar(0xE034, GlyphName(0xE034))
pen = C.glyphPen()
pen.moveTo((0,0))
pen.lineTo((0,1000))
pen.lineTo((DEFAULTS["barlines"]["hthick2"],1000))
pen.lineTo((DEFAULTS["barlines"]["hthick2"],0))
pen.closePath()
pen = None

C = F.createChar(0xE035, GlyphName(0xE035))
pen = C.glyphPen()
X = 0
pen.moveTo((X+0,0))
pen.lineTo((X+0,1000))
pen.lineTo((X+DEFAULTS["barlines"]["hthick2"],1000))
pen.lineTo((X+DEFAULTS["barlines"]["hthick2"],0))
pen.closePath()
X = DEFAULTS["barlines"]["hthick2"] + DEFAULTS["barlines"]["hsep"]
pen.moveTo((X+0,0))
pen.lineTo((X+0,1000))
pen.lineTo((X+DEFAULTS["barlines"]["hthick2"],1000))
pen.lineTo((X+DEFAULTS["barlines"]["hthick2"],0))
pen.closePath()
pen = None


# Repeats

def DrawCircle(pen, X, Y, R):
    pen.moveTo((X-R,Y))
    pen.curveTo(X-R,Y+0.6*R,X-0.6*R,Y+R,X,Y+R)
    pen.curveTo(X+0.6*R,Y+R,X+R,Y+0.6*R,X+R,Y)
    pen.curveTo(X+R,Y-0.6*R,X+0.6*R,Y-R,X,Y-R)
    pen.curveTo(X-0.6*R,Y-R,X-R,Y-0.6*R,X-R,Y)
    pen.closePath()

def DrawBar(pen, X, Y, YH, THICK):
    pen.moveTo((X+0,Y+0))
    pen.lineTo((X+0,Y+YH))
    pen.lineTo((X+THICK,Y+YH))
    pen.lineTo((X+THICK,Y+0))
    pen.closePath()

C = F.createChar(0xE044, GlyphName(0xE044))
pen = C.glyphPen()
DrawCircle(pen, 0, 0, DEFAULTS["barlines"]["repeat_diameter"]/2)
pen = None


C = F.createChar(0xE043, GlyphName(0xE043))
pen = C.glyphPen()
DrawCircle(pen, 0, 125+0*250, DEFAULTS["barlines"]["repeat_diameter"]/2)
DrawCircle(pen, 0, 125+1*250, DEFAULTS["barlines"]["repeat_diameter"]/2)
DrawCircle(pen, 0, 125+2*250, DEFAULTS["barlines"]["repeat_diameter"]/2)
DrawCircle(pen, 0, 125+3*250, DEFAULTS["barlines"]["repeat_diameter"]/2)
pen = None

C = F.createChar(0xE040, GlyphName(0xE040))
pen = C.glyphPen()
X = 0
DrawBar(pen, X, 0, 1000, DEFAULTS["barlines"]["hthick2"])
X += DEFAULTS["barlines"]["hthick2"] + DEFAULTS["barlines"]["hsep"]
DrawBar(pen, X, 0, 1000, DEFAULTS["barlines"]["hthick1"])
X += DEFAULTS["barlines"]["hthick1"] + DEFAULTS["barlines"]["hsep_dots"] + DEFAULTS["barlines"]["repeat_diameter"]/2
DrawCircle(pen, X, 125+0*250, DEFAULTS["barlines"]["repeat_diameter"]/2)
DrawCircle(pen, X, 125+1*250, DEFAULTS["barlines"]["repeat_diameter"]/2)
DrawCircle(pen, X, 125+2*250, DEFAULTS["barlines"]["repeat_diameter"]/2)
DrawCircle(pen, X, 125+3*250, DEFAULTS["barlines"]["repeat_diameter"]/2)
pen = None


C = F.createChar(0xE041, GlyphName(0xE041))
pen = C.glyphPen()
X = 0
DrawCircle(pen, X, 125+0*250, DEFAULTS["barlines"]["repeat_diameter"]/2)
DrawCircle(pen, X, 125+1*250, DEFAULTS["barlines"]["repeat_diameter"]/2)
DrawCircle(pen, X, 125+2*250, DEFAULTS["barlines"]["repeat_diameter"]/2)
DrawCircle(pen, X, 125+3*250, DEFAULTS["barlines"]["repeat_diameter"]/2)
X += DEFAULTS["barlines"]["hsep_dots"] + DEFAULTS["barlines"]["repeat_diameter"]/2
DrawBar(pen, X, 0, 1000, DEFAULTS["barlines"]["hthick1"])
X += DEFAULTS["barlines"]["hthick1"] + DEFAULTS["barlines"]["hsep"]
DrawBar(pen, X, 0, 1000, DEFAULTS["barlines"]["hthick2"])
pen = None

C = F.createChar(0xE042, GlyphName(0xE042))
pen = C.glyphPen()
X = 0
DrawCircle(pen, X, 125+0*250, DEFAULTS["barlines"]["repeat_diameter"]/2)
DrawCircle(pen, X, 125+1*250, DEFAULTS["barlines"]["repeat_diameter"]/2)
DrawCircle(pen, X, 125+2*250, DEFAULTS["barlines"]["repeat_diameter"]/2)
DrawCircle(pen, X, 125+3*250, DEFAULTS["barlines"]["repeat_diameter"]/2)
X += DEFAULTS["barlines"]["hsep_dots"] + DEFAULTS["barlines"]["repeat_diameter"]/2
DrawBar(pen, X, 0, 1000, DEFAULTS["barlines"]["hthick1"])
X += DEFAULTS["barlines"]["hthick1"] + DEFAULTS["barlines"]["hsep"]
DrawBar(pen, X, 0, 1000, DEFAULTS["barlines"]["hthick2"])
X += DEFAULTS["barlines"]["hthick2"] + DEFAULTS["barlines"]["hsep"]
DrawBar(pen, X, 0, 1000, DEFAULTS["barlines"]["hthick1"])
X += DEFAULTS["barlines"]["hthick1"] + DEFAULTS["barlines"]["hsep_dots"] + DEFAULTS["barlines"]["repeat_diameter"]/2
DrawCircle(pen, X, 125+0*250, DEFAULTS["barlines"]["repeat_diameter"]/2)
DrawCircle(pen, X, 125+1*250, DEFAULTS["barlines"]["repeat_diameter"]/2)
DrawCircle(pen, X, 125+2*250, DEFAULTS["barlines"]["repeat_diameter"]/2)
DrawCircle(pen, X, 125+3*250, DEFAULTS["barlines"]["repeat_diameter"]/2)
pen = None




X, Y = None, None
for A in F[GlyphName(0xE0A4)].anchorPoints:
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

    C = F.createChar(int(uni, 16), GlyphName(int(uni, 16)))
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



#flagInternalUp

C = F.createChar(0xE250, GlyphName(0xE250))
pen = C.glyphPen()
F[GlyphName(0xE240)].draw(pen)
pen = None






# Minim up

X, Y = None, None
for A in F[GlyphName(0xE0A3)].anchorPoints:
    if A[0] == 'stemUpSE' and A[1] == 'base':
        X, Y = A[2], A[3]

# Notehead with stem up
C = F.createChar(0xE1D3, GlyphName(0xE1D3))
pen = C.glyphPen()
F[GlyphName(0xE0A3)].draw(pen)
pen.moveTo((X,Y))
pen.lineTo((X-DEFAULTS["stemThickness"],Y))
pen.lineTo((X-DEFAULTS["stemThickness"],Y+DEFAULTS["stemHeight"]))
pen.lineTo((X,Y+DEFAULTS["stemHeight"]))
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
    C = F.createChar(int(uni, 16), GlyphName(int(uni, 16)))
    pen = C.glyphPen()
    F[GlyphName(0xE04A)].draw(pen)
    if uni_flag:
        try:
            F[GlyphName(int(uni_flag, 16))].draw(pen)       
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
for A in F[GlyphName(0xE0A4)].anchorPoints:
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

    C = F.createChar(int(uni, 16), GlyphName(int(uni, 16)))
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



# Minim

X, Y = None, None
for A in F[GlyphName(0xE0A3)].anchorPoints:
    if A[0] == 'stemDownNW' and A[1] == 'base':
        X, Y = A[2], A[3]

# Minim with stem down
C = F.createChar(0xE1D4, GlyphName(0xE1D4))
pen = C.glyphPen()
F[GlyphName(0xE0A3)].draw(pen)
pen.moveTo((X,Y))
pen.lineTo((X+DEFAULTS["stemThickness"],Y))
pen.lineTo((X+DEFAULTS["stemThickness"],Y-DEFAULTS["stemHeight"]))
pen.lineTo((X,Y-DEFAULTS["stemHeight"]))
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
    C = F.createChar(int(uni, 16), GlyphName(int(uni, 16)))
    pen = C.glyphPen()
    F[GlyphName(0xE0A4)].draw(pen)
    if uni_flag:
        F[GlyphName(int(uni_flag, 16))].draw(pen)
    pen.moveTo((X,Y))
    pen.lineTo((X+DEFAULTS["stemThickness"],Y))
    pen.lineTo((X+DEFAULTS["stemThickness"],Y-DEFAULTS["stemHeight"]))
    pen.lineTo((X,Y-DEFAULTS["stemHeight"]))
    pen.closePath()
    C.removeOverlap()
    pen = None
      

#flagInternalDown

C = F.createChar(0xE251, GlyphName(0xE251))
pen = C.glyphPen()
F[GlyphName(0xE241)].draw(pen)
pen = None




# accidental sharp
X = 0
Y = 0
C = F.createChar(0xE262, GlyphName(0xE262))
pen = C.glyphPen()
# Upright 1
pen.moveTo((X+( DEFAULTS["sharp"]["hsep"]-DEFAULTS["sharp"]["hthick"])//2,Y+(DEFAULTS["sharp"]["h"])//2))
pen.lineTo((X+( DEFAULTS["sharp"]["hsep"]+DEFAULTS["sharp"]["hthick"])//2,Y+(DEFAULTS["sharp"]["h"])//2))
pen.lineTo((X+( DEFAULTS["sharp"]["hsep"]+DEFAULTS["sharp"]["hthick"])//2,Y-(DEFAULTS["sharp"]["h"])//2))
pen.lineTo((X+( DEFAULTS["sharp"]["hsep"]-DEFAULTS["sharp"]["hthick"])//2,Y-(DEFAULTS["sharp"]["h"])//2))
pen.closePath()

# Upright 2
pen.moveTo((X+(-DEFAULTS["sharp"]["hsep"]-DEFAULTS["sharp"]["hthick"])//2,Y+(DEFAULTS["sharp"]["h"])//2))
pen.lineTo((X+(-DEFAULTS["sharp"]["hsep"]+DEFAULTS["sharp"]["hthick"])//2,Y+(DEFAULTS["sharp"]["h"])//2))
pen.lineTo((X+(-DEFAULTS["sharp"]["hsep"]+DEFAULTS["sharp"]["hthick"])//2,Y-(DEFAULTS["sharp"]["h"])//2))
pen.lineTo((X+(-DEFAULTS["sharp"]["hsep"]-DEFAULTS["sharp"]["hthick"])//2,Y-(DEFAULTS["sharp"]["h"])//2))
pen.closePath()

# Horizontal 1
pen.moveTo((X-DEFAULTS["sharp"]["w"],Y+( DEFAULTS["sharp"]["vsep"]+DEFAULTS["sharp"]["vthick"]-DEFAULTS["sharp"]["vdrop"])//2))
pen.lineTo((X+DEFAULTS["sharp"]["w"],Y+( DEFAULTS["sharp"]["vsep"]+DEFAULTS["sharp"]["vthick"]+DEFAULTS["sharp"]["vdrop"])//2))
pen.lineTo((X+DEFAULTS["sharp"]["w"],Y+( DEFAULTS["sharp"]["vsep"]-DEFAULTS["sharp"]["vthick"]+DEFAULTS["sharp"]["vdrop"])//2))
pen.lineTo((X-DEFAULTS["sharp"]["w"],Y+( DEFAULTS["sharp"]["vsep"]-DEFAULTS["sharp"]["vthick"]-DEFAULTS["sharp"]["vdrop"])//2))
pen.closePath()

# Horizontal 2
pen.moveTo((X-DEFAULTS["sharp"]["w"],Y+(-DEFAULTS["sharp"]["vsep"]+DEFAULTS["sharp"]["vthick"]-DEFAULTS["sharp"]["vdrop"])//2))
pen.lineTo((X+DEFAULTS["sharp"]["w"],Y+(-DEFAULTS["sharp"]["vsep"]+DEFAULTS["sharp"]["vthick"]+DEFAULTS["sharp"]["vdrop"])//2))
pen.lineTo((X+DEFAULTS["sharp"]["w"],Y+(-DEFAULTS["sharp"]["vsep"]-DEFAULTS["sharp"]["vthick"]+DEFAULTS["sharp"]["vdrop"])//2))
pen.lineTo((X-DEFAULTS["sharp"]["w"],Y+(-DEFAULTS["sharp"]["vsep"]-DEFAULTS["sharp"]["vthick"]-DEFAULTS["sharp"]["vdrop"])//2))
pen.closePath()

C.removeOverlap()
C.left_side_bearing = 0
C.right_side_bearing = 0
C.autoHint()
pen = None



# accidental Natural
X = 0
Y = 0
C = F.createChar(0xE261, GlyphName(0xE261))
pen = C.glyphPen()
# Upright 1
pen.moveTo((X+(-DEFAULTS["natural"]["hsep"]-DEFAULTS["natural"]["hthick"])//2,Y+(DEFAULTS["natural"]["h"])//2))
pen.lineTo((X+(-DEFAULTS["natural"]["hsep"]+DEFAULTS["natural"]["hthick"])//2,Y+(DEFAULTS["natural"]["h"])//2))
pen.lineTo((X+(-DEFAULTS["natural"]["hsep"]+DEFAULTS["natural"]["hthick"])//2,Y-(DEFAULTS["natural"]["vsep"])//2))
pen.lineTo((X+(-DEFAULTS["natural"]["hsep"]-DEFAULTS["natural"]["hthick"])//2,Y-(DEFAULTS["natural"]["vsep"])//2))
pen.closePath()

# Upright 2
pen.moveTo((X+( DEFAULTS["natural"]["hsep"]-DEFAULTS["natural"]["hthick"])//2,Y+(DEFAULTS["natural"]["vsep"])//2))
pen.lineTo((X+( DEFAULTS["natural"]["hsep"]+DEFAULTS["natural"]["hthick"])//2,Y+(DEFAULTS["natural"]["vsep"])//2))
pen.lineTo((X+( DEFAULTS["natural"]["hsep"]+DEFAULTS["natural"]["hthick"])//2,Y-(DEFAULTS["natural"]["h"])//2))
pen.lineTo((X+( DEFAULTS["natural"]["hsep"]-DEFAULTS["natural"]["hthick"])//2,Y-(DEFAULTS["natural"]["h"])//2))
pen.closePath()

# Horizontal 1
pen.moveTo((X-(DEFAULTS["natural"]["hsep"]+DEFAULTS["natural"]["hthick"])//2,Y+( DEFAULTS["natural"]["vsep"]+DEFAULTS["natural"]["vthick"]-DEFAULTS["natural"]["vdrop"])//2))
pen.lineTo((X+(DEFAULTS["natural"]["hsep"]+DEFAULTS["natural"]["hthick"])//2,Y+( DEFAULTS["natural"]["vsep"]+DEFAULTS["natural"]["vthick"]+DEFAULTS["natural"]["vdrop"])//2))
pen.lineTo((X+(DEFAULTS["natural"]["hsep"]+DEFAULTS["natural"]["hthick"])//2,Y+( DEFAULTS["natural"]["vsep"]-DEFAULTS["natural"]["vthick"]+DEFAULTS["natural"]["vdrop"])//2))
pen.lineTo((X-(DEFAULTS["natural"]["hsep"]+DEFAULTS["natural"]["hthick"])//2,Y+( DEFAULTS["natural"]["vsep"]-DEFAULTS["natural"]["vthick"]-DEFAULTS["natural"]["vdrop"])//2))
pen.closePath()

# Horizontal 2
pen.moveTo((X-(DEFAULTS["natural"]["hsep"]+DEFAULTS["natural"]["hthick"])//2,Y+(-DEFAULTS["natural"]["vsep"]+DEFAULTS["natural"]["vthick"]-DEFAULTS["natural"]["vdrop"])//2))
pen.lineTo((X+(DEFAULTS["natural"]["hsep"]+DEFAULTS["natural"]["hthick"])//2,Y+(-DEFAULTS["natural"]["vsep"]+DEFAULTS["natural"]["vthick"]+DEFAULTS["natural"]["vdrop"])//2))
pen.lineTo((X+(DEFAULTS["natural"]["hsep"]+DEFAULTS["natural"]["hthick"])//2,Y+(-DEFAULTS["natural"]["vsep"]-DEFAULTS["natural"]["vthick"]+DEFAULTS["natural"]["vdrop"])//2))
pen.lineTo((X-(DEFAULTS["natural"]["hsep"]+DEFAULTS["natural"]["hthick"])//2,Y+(-DEFAULTS["natural"]["vsep"]-DEFAULTS["natural"]["vthick"]-DEFAULTS["natural"]["vdrop"])//2))
pen.closePath()

C.removeOverlap()
C.left_side_bearing = 0
C.right_side_bearing = 0
C.autoHint()
pen = None


# Rests
C = F.createChar(0xE4E1, GlyphName(0xE4E1))
pen = C.glyphPen()
pen.moveTo((0,750))
pen.lineTo((DEFAULTS["restLonga"]["w"],750))
pen.lineTo((DEFAULTS["restLonga"]["w"],250))
pen.lineTo((0,250))
pen.closePath()
pen=None

C = F.createChar(0xE4E2, GlyphName(0xE4E2))
pen = C.glyphPen()
pen.moveTo((0,750))
pen.lineTo((DEFAULTS["restLonga"]["w"],750))
pen.lineTo((DEFAULTS["restLonga"]["w"],500))
pen.lineTo((0,500))
pen.closePath()
pen=None

C = F.createChar(0xE4E3, GlyphName(0xE4E3))
pen = C.glyphPen()
pen.moveTo((0,500))
pen.lineTo((DEFAULTS["rest"]["w"],500))
pen.lineTo((DEFAULTS["rest"]["w"],500-DEFAULTS["rest"]["h"]))
pen.lineTo((0,500-DEFAULTS["rest"]["h"]))
pen.closePath()
pen=None

C = F.createChar(0xE4E4, GlyphName(0xE4E4))
pen = C.glyphPen()
pen.moveTo((0,500+DEFAULTS["rest"]["h"]))
pen.lineTo((DEFAULTS["rest"]["w"],500+DEFAULTS["rest"]["h"]))
pen.lineTo((DEFAULTS["rest"]["w"],500))
pen.lineTo((0,500))
pen.closePath()
pen=None

F.save("samuel-12.sfd")
"""


with open('s2.py', 'w') as f_scr:
    f_scr.write(S)
subprocess.run(['fontforge', '--script', 's2.py'])




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
          f = fontforge.open("samuel-12.sfd")
          """.format(__DST__, name) + """
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
                          f2.write('    <a n="{0}" x="{2:0.1f}" y="{3:0.1f}"/>\\n'.format(*ANCHOR))
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




# Create a SMuFL metadata file

S = """

import json

D = {}

"""
S += "D.update({'fontName': " + '"{0}"'.format(__NAME__) + "})\n"
S += "D.update({'fontVersion': " + '"{0}"'.format(__VERSION__) + "})\n"

S += """
D.update({'engravingDefaults': {}})
D.update({'glyphAdvanceWidths': {}})
D.update({'glyphBBoxes': {}})
"""
S += """

with open("{0}", "w") as f:
    json.dump(D, f, indent = "\t")

""".format("samuel-metadata.json")

with open('s7.py', 'w') as f_scr:
    f_scr.write(S)
subprocess.run(['fontforge', '--script', 's7.py'])






# Put the font into the verovio data directory.

P = pathlib.Path(venv.sysconfig.get_path('platlib'))

if not P.joinpath('verovio').is_dir():
    print('Could not find verovio installed in this virtual environment. Try:\n\n    pip install verovio\n')
    sys.exit(-1)

if not os.access(P.joinpath('verovio'), os.W_OK):
    print('Do not have write access to the verovio installation. Most likely you are running\nfrom the main installation of python rather than a virtual environment.\nPlease call this script from a virtual environment. See:\n\n    https://docs.python.org/3/library/venv.html\n')
    sys.exit(-1)

CreateVerovioFont("samuel-12.sfd", __NAME__, P.joinpath("verovio", "data"))



# Run Verovio to render the test score
import verovio

V = verovio.toolkit()
V.loadFile('test1.musicxml')
V.setFont("Samuel")   # use the font that we've just created
V.renderToSVGFile('test1out.svg')


# Change from SVG to PNG. There are surprisingly few cross-platform ways of doing this.
# Reportlab.graphics.renderPM gives terrible results - don't use it! This method using
# inkscape is okay, but it requires installing inkscape.



P_IN = pathlib.Path.cwd().resolve().joinpath("test1out.svg")
P_OUT = pathlib.Path.cwd().resolve().joinpath("test1out.png")

subprocess.run(['inkscape', '-o', str(P_OUT), '--export-overwrite', '--export-type=png', '--export-area={0}:{1}:{2}:{3}'.format(0, 0, 1000, 500), '--export-background=white', str(P_IN)])

