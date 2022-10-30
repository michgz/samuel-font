# Build the font, adding geometric glyphs and filling out everything that needs
# to be filled out


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
              'beamSpacing': 25,   'beamThickness': 100,   \
              # "flags" applies specifically to Straight flags (variant glyphs).
              "flags": {"h": 80, "w": 180, "drop": 70, "sep": 40},    \
              # "flags_c" is the curvy (non-variant) flags.
              "flags_c": {"voffset": 190},    \
              "sharp":   {"h": 480, "w": 105, "hthick": 16, "vthick": 80, "hsep": 75, "vsep": 190, "vdrop": 60},  \
              "natural": {"h": 540,           "hthick": 20, "vthick": 80, "hsep": 60, "vsep": 200, "vdrop": 50},  \
              "barlines": {"hthick1": 10, "hthick2": 60, "hsep": 20, "hsep_dots": 20, "repeat_diameter": 110},   \
              "restLonga": {"w": 210},   \
              "rest": {"w": 368, "h": 125},    \
              "staff": {"narrow": 200, "mid": 300, "wide": 400},     \
              "leger": {"narrow": 200, "mid": 300, "wide": 400},     \
              "dot_diameter": 70,       \
              # overlap is how much beyond the period to extend the stem
              "quaver_rest": {"period": 250, "overlap": 55},    \
              "cut_time": {"x": 250, "thickness": 35, "y1": -350, "y2": 350},   \
          }


def build_font(in_path, out_path):

    S = """
    
    __INPUT_PATH__ = "{0}"
    """.format(str(in_path)) + \
    """
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

    F = fontforge.open(__INPUT_PATH__)

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


    #Augmentation dot (used for dotted notes)
    C = F.createChar(0xE1E7, GlyphName(0xE1E7))
    pen = C.glyphPen()
    DrawCircle(pen, 0, 0, DEFAULTS["dot_diameter"]/2)
    pen = None


    X, Y = None, None
    for A in F[GlyphName(0xE0A4)].anchorPoints:
        if A[0] == 'stemUpSE' and A[1] == 'base':
            X, Y = A[2], A[3]


    # Override the X, Y defined above. At least for Verovio, the stemUpNW point needs to
    # be near (0,0)
    X = 0
    Y = -DEFAULTS["stemHeight"]

    # Now do all the up flags (straight variants)
    FLAGS_UP = [
        ("flag8thUpStraight", 1, "F410"),
        ("flag16thUpStraight", 2, "F411"),
        ("flag32ndUpStraight", 3, "F412"),
        ("flag64thUpStraight", 4, "F413"),
        ("flag128thUpStraight", 5, "F414"),
        ("flag256thUpStraight", 6, "F415"),
        ("flag512thUpStraight", 7, "F416"),
        ("flag1024thUpStraight", 8, "F417")]


    for glyph_name, flag_count, uni in FLAGS_UP:

        C = F.createChar(int(uni, 16), glyph_name)
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

        C.left_side_bearing = 0
        C.right_side_bearing = 0
        C.addAnchorPoint("stemUpNW", "base", X, Y+DEFAULTS["stemHeight"])
        C.autoHint()
        pen = None



    #flagInternalUp (straight variant)

    C = F.createChar(0xF418, "flagInternalUpStraight")  # This name doesn't exist in the SMuFL standard!
    pen = C.glyphPen()
    F["flag8thUpStraight"].draw(pen)
    pen = None


    # flag internal up is a reflection of the down
    C = F.createChar(0xE250, GlyphName(0xE250))
    P = C.glyphPen()
    F["flagInternalDown"].draw(P)
    C.transform((1,0,0,-1,0,0))   # reflect around x axis
    C.correctDirection()          # Correct the direction
    C.left_side_bearing = 0
    C.right_side_bearing = 0
    C.autoHint()
    P = None


    # Do all the up flags (non-variants)
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


        Y_correction = -250 if flag_count == 1 else -500
        # Sort this out!! This is just a correction so things don't look wildly
        # wrong, but really should be matching the positioning in Bravura.


        C = F.createChar(int(uni, 16), GlyphName(int(uni, 16)))
        pen = C.glyphPen()
        
        # Quavers and semiquavers use the standard stem height. After that, need to
        # start extending.
        if flag_count == 1:
            flag_base = 0
        else:
            flag_base = 1

        for J in range(flag_count):
            CNT = F["flagInternalUp"].layers[1][0]    # First contour of the foreground layer
            CNT.transform((1,0,0,1,X-DEFAULTS["stemThickness"],Y+Y_correction + DEFAULTS["stemHeight"] + (DEFAULTS["flags_c"]["voffset"]*(J+flag_base))))
            CNT.draw(pen)

        # Draw a partial stem between the mid-points of the extreme flags
        if flag_count >= 2:
            pen.moveTo((X                          ,                          Y+Y_correction+DEFAULTS["stemHeight"]+(DEFAULTS["flags_c"]["voffset"])*(flag_base-1)           -0.5*DEFAULTS["flags_c"]["voffset"]   ))
            pen.lineTo((X-DEFAULTS["stemThickness"],                          Y+Y_correction+DEFAULTS["stemHeight"]+(DEFAULTS["flags_c"]["voffset"])*(flag_base-1)           -0.5*DEFAULTS["flags_c"]["voffset"]   ))
            pen.lineTo((X-DEFAULTS["stemThickness"],                          Y+Y_correction+DEFAULTS["stemHeight"]+(DEFAULTS["flags_c"]["voffset"])*(flag_base+flag_count-0)+0.5*DEFAULTS["flags_c"]["voffset"]   ))
            pen.lineTo((X                          ,                          Y+Y_correction+DEFAULTS["stemHeight"]+(DEFAULTS["flags_c"]["voffset"])*(flag_base+flag_count-0)+0.5*DEFAULTS["flags_c"]["voffset"]   ))
            pen.closePath()
            
            C.removeOverlap()


        C.left_side_bearing = 0
        C.right_side_bearing = 0
        C.addAnchorPoint("stemUpNW", "base", X, Y+Y_correction+DEFAULTS["stemHeight"])
        C.autoHint()
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





    X, Y = None, None
    for A in F[GlyphName(0xE0A4)].anchorPoints:
        if A[0] == 'stemUpSE' and A[1] == 'base':
            X, Y = A[2], A[3]

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
        F[GlyphName(0xE0A4)].draw(pen)
        if uni_flag:
            try:
                CNT = F[GlyphName(int(uni_flag, 16))].layers[1][0]    # First contour of the foreground layer
            except TypeError:
                print('uni' + uni_flag)
                raise
            CNT.transform((1,0,0,1,X-DEFAULTS["stemThickness"],Y+DEFAULTS["stemHeight"]))
            CNT.draw(pen)
        pen.moveTo((X,Y))
        pen.lineTo((X-DEFAULTS["stemThickness"],Y))
        pen.lineTo((X-DEFAULTS["stemThickness"],Y+DEFAULTS["stemHeight"]))
        pen.lineTo((X,Y+DEFAULTS["stemHeight"]))
        pen.closePath()
        C.removeOverlap()
        C.left_side_bearing = 0
        C.right_side_bearing = 0
        C.autoHint()
        pen = None





    X, Y = None, None
    for A in F[GlyphName(0xE0A4)].anchorPoints:
        if A[0] == 'stemDownNW' and A[1] == 'base':
            X, Y = A[2], A[3]
            
         
    # Override the X, Y defined above. At least for Verovio, the stemDownSW point needs to
    # be near (0,0)
    X = 0
    Y = DEFAULTS["stemHeight"]
         
         
            

    # Now do all the down flags (straight variants)
    FLAGS_DOWN = [
        ("flag8thDownStraight", 1, "F419"),
        ("flag16thDownStraight", 2, "F41A"),
        ("flag32ndDownStraight", 3, "F41B"),
        ("flag64thDownStraight", 4, "F41C"),
        ("flag128thDownStraight", 5, "F41D"),
        ("flag256thDownStraight", 6, "F41E"),
        ("flag512thDownStraight", 7, "F41F"),
        ("flag1024thDownStraight", 8, "F420")]


    for glyph_name, flag_count, uni in FLAGS_DOWN:

        C = F.createChar(int(uni, 16), glyph_name)
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

        C.left_side_bearing = 0
        C.right_side_bearing = 0
        C.addAnchorPoint("stemDownSW", "base", X, Y-DEFAULTS["stemHeight"])
        C.autoHint()
        pen = None


    # Do all the down flags (non-variants)
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


        Y_correction = 250 if flag_count == 1 else 500
        # Sort this out!! This is just a correction so things don't look wildly
        # wrong, but really should be matching the positioning in Bravura.



        C = F.createChar(int(uni, 16), GlyphName(int(uni, 16)))
        pen = C.glyphPen()
        
        # Quavers and semiquavers use the standard stem height. After that, need to
        # start extending.
        if flag_count == 1:
            flag_base = 0
        else:
            flag_base = 1

        for J in range(flag_count):
            CNT = F["flagInternalDown"].layers[1][0]    # First contour of the foreground layer
            CNT.transform((1,0,0,1,X,Y+Y_correction - DEFAULTS["stemHeight"] + (DEFAULTS["flags_c"]["voffset"]*(-J+flag_base))))
            CNT.draw(pen)

        # Draw a partial stem between the mid-points of the extreme flags
        if flag_count >= 2:
            pen.moveTo((X                          ,                          Y+Y_correction-DEFAULTS["stemHeight"]+(DEFAULTS["flags_c"]["voffset"])*(flag_base)             +0.5*DEFAULTS["flags_c"]["voffset"]   ))
            pen.lineTo((X+DEFAULTS["stemThickness"],                          Y+Y_correction-DEFAULTS["stemHeight"]+(DEFAULTS["flags_c"]["voffset"])*(flag_base)             +0.5*DEFAULTS["flags_c"]["voffset"]   ))
            pen.lineTo((X+DEFAULTS["stemThickness"],                          Y+Y_correction-DEFAULTS["stemHeight"]+(DEFAULTS["flags_c"]["voffset"])*(flag_base-flag_count+0)-0.5*DEFAULTS["flags_c"]["voffset"]   ))
            pen.lineTo((X                          ,                          Y+Y_correction-DEFAULTS["stemHeight"]+(DEFAULTS["flags_c"]["voffset"])*(flag_base-flag_count+0)-0.5*DEFAULTS["flags_c"]["voffset"]   ))
            pen.closePath()
            
            C.removeOverlap()

        C.left_side_bearing = 0
        C.right_side_bearing = 0
        C.addAnchorPoint("stemDownSW", "base", X, Y+Y_correction-DEFAULTS["stemHeight"])
        C.autoHint()
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
    C.left_side_bearing = 0
    C.right_side_bearing = 0
    C.autoHint()
    pen = None



    X, Y = None, None
    for A in F[GlyphName(0xE0A4)].anchorPoints:
        if A[0] == 'stemDownNW' and A[1] == 'base':
            X, Y = A[2], A[3]


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
            CNT = F[GlyphName(int(uni_flag, 16))].layers[1][0]    # First contour of the foreground layer
            CNT.transform((1,0,0,1,X,Y-DEFAULTS["stemHeight"]))
            CNT.draw(pen)
        pen.moveTo((X,Y))
        pen.lineTo((X+DEFAULTS["stemThickness"],Y))
        pen.lineTo((X+DEFAULTS["stemThickness"],Y-DEFAULTS["stemHeight"]))
        pen.lineTo((X,Y-DEFAULTS["stemHeight"]))
        pen.closePath()
        C.removeOverlap()
        C.left_side_bearing = 0
        C.right_side_bearing = 0
        C.autoHint()
        pen = None
          

    #flagInternalDown

    C = F.createChar(0xF421, "flagInternalDownStraight")   # This name doesn't exist in the SMuFL standard!
    pen = C.glyphPen()
    F["flag8thDownStraight"].draw(pen)
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
    pen.moveTo((0,500))
    pen.lineTo((DEFAULTS["restLonga"]["w"],500))
    pen.lineTo((DEFAULTS["restLonga"]["w"],0))
    pen.lineTo((0,0))
    pen.closePath()
    C.left_side_bearing = 0
    C.right_side_bearing = 0
    C.autoHint()
    pen=None

    C = F.createChar(0xE4E2, GlyphName(0xE4E2))
    pen = C.glyphPen()
    pen.moveTo((0,250))
    pen.lineTo((DEFAULTS["restLonga"]["w"],250))
    pen.lineTo((DEFAULTS["restLonga"]["w"],0))
    pen.lineTo((0,0))
    pen.closePath()
    C.left_side_bearing = 0
    C.right_side_bearing = 0
    C.autoHint()
    pen=None

    C = F.createChar(0xE4E3, GlyphName(0xE4E3))
    pen = C.glyphPen()
    pen.moveTo((0,0))
    pen.lineTo((DEFAULTS["rest"]["w"],0))
    pen.lineTo((DEFAULTS["rest"]["w"],0-DEFAULTS["rest"]["h"]))
    pen.lineTo((0,0-DEFAULTS["rest"]["h"]))
    pen.closePath()
    C.left_side_bearing = 0
    C.right_side_bearing = 0
    C.autoHint()
    pen=None

    C = F.createChar(0xE4E4, GlyphName(0xE4E4))
    pen = C.glyphPen()
    pen.moveTo((0,0+DEFAULTS["rest"]["h"]))
    pen.lineTo((DEFAULTS["rest"]["w"],0+DEFAULTS["rest"]["h"]))
    pen.lineTo((DEFAULTS["rest"]["w"],0))
    pen.lineTo((0,0))
    pen.closePath()
    C.left_side_bearing = 0
    C.right_side_bearing = 0
    C.autoHint()
    pen=None

    # Reverse the quaver rest to get an "old" crotchet

    C = F.createChar(0xE4F2, GlyphName(0xE4F2))
    pen = C.glyphPen()
    F[GlyphName(0xE4E6)].draw(pen)
    C.transform( (-1,0,0,1,0,0) )  # reverse X direction, keep Y direction.
    C.left_side_bearing = 0
    C.right_side_bearing = 0
    C.autoHint()
    pen = None

    # Now, optionally replace the crotchet with another style.
    #NEW_CROTCHET = 0xE4F2
    #NEW_CROTCHET = 0xE4F6
    NEW_CROTCHET = None
    if NEW_CROTCHET is not None:
        F.removeGlyph(0xE4E5)
        C = F.createChar(0xE4E5, "restQuarter")
        pen = C.glyphPen()
        F[GlyphName(NEW_CROTCHET)].draw(pen)
        C.left_side_bearing = int(F[GlyphName(NEW_CROTCHET)].left_side_bearing)
        C.right_side_bearing = int(F[GlyphName(NEW_CROTCHET)].right_side_bearing)
        C.autoHint()
        pen = None


    # Staves (only the 5-line ones and leger lines)

    C = F.createChar(0xE014, GlyphName(0xE014))
    pen = C.glyphPen()
    for Y in [0, 250, 500, 750, 1000]:
        pen.moveTo((0,Y+DEFAULTS["staffLineThickness"]/2))
        pen.lineTo((DEFAULTS["staff"]["mid"],Y+DEFAULTS["staffLineThickness"]/2))
        pen.lineTo((DEFAULTS["staff"]["mid"],Y-DEFAULTS["staffLineThickness"]/2))
        pen.lineTo((0,Y-DEFAULTS["staffLineThickness"]/2))
        pen.closePath()
    C.left_side_bearing = 0
    C.right_side_bearing = 0
    C.autoHint()
    pen = None

    C = F.createChar(0xE020, GlyphName(0xE020))
    pen = C.glyphPen()
    for Y in [0, 250, 500, 750, 1000]:
        pen.moveTo((0,Y+DEFAULTS["staffLineThickness"]/2))
        pen.lineTo((DEFAULTS["staff"]["narrow"],Y+DEFAULTS["staffLineThickness"]/2))
        pen.lineTo((DEFAULTS["staff"]["narrow"],Y-DEFAULTS["staffLineThickness"]/2))
        pen.lineTo((0,Y-DEFAULTS["staffLineThickness"]/2))
        pen.closePath()
    C.left_side_bearing = 0
    C.right_side_bearing = 0
    C.autoHint()
    pen = None

    C = F.createChar(0xE01A, GlyphName(0xE01A))
    pen = C.glyphPen()
    for Y in [0, 250, 500, 750, 1000]:
        pen.moveTo((0,Y+DEFAULTS["staffLineThickness"]/2))
        pen.lineTo((DEFAULTS["staff"]["wide"],Y+DEFAULTS["staffLineThickness"]/2))
        pen.lineTo((DEFAULTS["staff"]["wide"],Y-DEFAULTS["staffLineThickness"]/2))
        pen.lineTo((0,Y-DEFAULTS["staffLineThickness"]/2))
        pen.closePath()
    C.left_side_bearing = 0
    C.right_side_bearing = 0
    C.autoHint()
    pen = None


    C = F.createChar(0xE022, GlyphName(0xE022))
    pen = C.glyphPen()
    for Y in [0]:
        pen.moveTo((0,Y+DEFAULTS["staffLineThickness"]/2))
        pen.lineTo((DEFAULTS["leger"]["mid"],Y+DEFAULTS["staffLineThickness"]/2))
        pen.lineTo((DEFAULTS["leger"]["mid"],Y-DEFAULTS["staffLineThickness"]/2))
        pen.lineTo((0,Y-DEFAULTS["staffLineThickness"]/2))
        pen.closePath()
    C.left_side_bearing = 0
    C.right_side_bearing = 0
    C.autoHint()
    pen = None

    C = F.createChar(0xE024, GlyphName(0xE024))
    pen = C.glyphPen()
    for Y in [0]:
        pen.moveTo((0,Y+DEFAULTS["staffLineThickness"]/2))
        pen.lineTo((DEFAULTS["leger"]["narrow"],Y+DEFAULTS["staffLineThickness"]/2))
        pen.lineTo((DEFAULTS["leger"]["narrow"],Y-DEFAULTS["staffLineThickness"]/2))
        pen.lineTo((0,Y-DEFAULTS["staffLineThickness"]/2))
        pen.closePath()
    C.left_side_bearing = 0
    C.right_side_bearing = 0
    C.autoHint()
    pen = None

    C = F.createChar(0xE023, GlyphName(0xE023))
    pen = C.glyphPen()
    for Y in [0]:
        pen.moveTo((0,Y+DEFAULTS["staffLineThickness"]/2))
        pen.lineTo((DEFAULTS["leger"]["wide"],Y+DEFAULTS["staffLineThickness"]/2))
        pen.lineTo((DEFAULTS["leger"]["wide"],Y-DEFAULTS["staffLineThickness"]/2))
        pen.lineTo((0,Y-DEFAULTS["staffLineThickness"]/2))
        pen.closePath()
    C.left_side_bearing = 0
    C.right_side_bearing = 0
    C.autoHint()
    pen = None

    # Rest + leger line combinations

    C = F.createChar(0xE4F4, GlyphName(0xE4F4))
    pen = C.glyphPen()
    F[GlyphName(0xE4E3)].draw(pen)
    F[GlyphName(0xE022)].draw(pen)
    C.left_side_bearing = 0
    C.right_side_bearing = 0
    C.autoHint()
    pen = None

    C = F.createChar(0xE4F5, GlyphName(0xE4F5))
    pen = C.glyphPen()
    F[GlyphName(0xE4E4)].draw(pen)
    F[GlyphName(0xE022)].draw(pen)
    C.left_side_bearing = 0
    C.right_side_bearing = 0
    C.autoHint()
    pen = None



    # Now do the fraction-of-quaver rests. This needs quite a bit of calculation.

    # First, find the NE and SE corners of the glyph. These will determine the slope of additional
    # segments
    NE = None
    SE = None
    GLIF = F[GlyphName(0xE4E6)]
    for CONTOUR in GLIF.foreground:
        for POINT in CONTOUR:
            if NE is None:
                NE = (POINT.x, POINT.y)
            else:
                if POINT.x+POINT.y > NE[0]+NE[1]:
                    NE = (POINT.x, POINT.y)
            if SE is None:
                SE = (POINT.x, POINT.y)
            else:
                if POINT.x-POINT.y > SE[0]-SE[1]:
                    SE = (POINT.x, POINT.y)

    DELTA_Y = float(DEFAULTS["quaver_rest"]["period"])


    DELTA_X = DELTA_Y * (NE[0] - SE[0]) / (NE[1] - SE[1])


    QUAVERS = [(0xE4E7, 1),
               (0xE4E8, 2),
               (0xE4E9, 3),
               (0xE4EA, 4),
               (0xE4EB, 5),
               (0xE4EC, 6),
               (0xE4ED, 7)]

    for Q in QUAVERS:

        # Now create the layer to repeat

        L = GLIF.foreground
        (xa, ya, xb, yb) = L.boundingBox()


        # Add a contour, which specifies the intersection

        ya = yb - DEFAULTS["quaver_rest"]["period"] - DEFAULTS["quaver_rest"]["overlap"]

        R = fontforge.contour()
        R.moveTo(xa, ya)
        R.lineTo(xa, yb)
        R.lineTo(xb, yb)
        R.lineTo(xb, ya)
        R.closed = True
        L += R

        # Intersect with the new contour
        L.intersect()

        C = F.createChar(Q[0], GlyphName(Q[0]))
        P = C.glyphPen()
        F[GlyphName(0xE4E6)].draw(P)
        for _ in range(Q[1]):
            L.transform((1,0,0,1,DELTA_X,DELTA_Y))
            L.draw(P)
        C.removeOverlap()
        C.left_side_bearing = 0
        C.right_side_bearing = 0
        C.autoHint()
        P = None


    # Turn all the "above" articulations upside down to form the "below" articulations.
    
    
    ARTICS = [(0xE4A1, "articAccentBelow"),
              (0xE4A3, "articStaccatoBelow"),
              (0xE4A5, "articTenutoBelow"),
              (0xE4A7, "articStaccatissimoBelow")]
              
    for A in ARTICS:
        if GlyphName(A[0] - 1) in F:
            C = F.createChar(A[0], GlyphName(A[0]))
            P = C.glyphPen()
            F[GlyphName(A[0] - 1)].draw(P)   # the "Above" variant is always 1 less
            C.transform((1,0,0,-1,0,0))    # Reflect around the x axis
            C.left_side_bearing = 0
            C.right_side_bearing = 0
            C.autoHint()
            P = None
    
    
    
    # Create combined dynamics markings
    
    # omit pp and ff, since they are already existing in the font.
    DYNAM = [(0xE52A, [0xE520, 0xE520, 0xE520]),
             (0xE529, [0xE520, 0xE520, 0xE520, 0xE520]),
             (0xE528, [0xE520, 0xE520, 0xE520, 0xE520, 0xE520]),
             (0xE527, [0xE520, 0xE520, 0xE520, 0xE520, 0xE520, 0xE520]),
             (0xE530, [0xE522, 0xE522, 0xE522]),
             (0xE531, [0xE522, 0xE522, 0xE522, 0xE522]),
             (0xE532, [0xE522, 0xE522, 0xE522, 0xE522, 0xE522]),
             (0xE533, [0xE522, 0xE522, 0xE522, 0xE522, 0xE522, 0xE522]),
             (0xE534, [0xE522, 0xE520]),
             (0xE535, [0xE522, 0xE525]),
             (0xE536, [0xE524, 0xE522]),
             (0xE537, [0xE524, 0xE522, 0xE520]),
             (0xE538, [0xE524, 0xE522, 0xE520, 0xE520]),
             (0xE539, [0xE524, 0xE522, 0xE525]),
             (0xE53A, [0xE524, 0xE522, 0xE525, 0xE520]),
             (0xE53B, [0xE524, 0xE522, 0xE522, 0xE525]),
             (0xE53C, [0xE523, 0xE522]),
             (0xE53D, [0xE523, 0xE522, 0xE525]),
             (0xE52C, [0xE521, 0xE520]),
             (0xE52D, [0xE521, 0xE522]),
             (0xE52E, [0xE520, 0xE522])]

    
    
    
    for DD in DYNAM:
        C = F.createChar(DD[0], GlyphName(DD[0]))
        P = C.glyphPen()
        
        X = 0
        
        for I, CC in enumerate(DD[1]):
        
            #print("Sub glyph ", I)
            #print("------------")
            #print("Bounding box: ", F[GlyphName(CC)].boundingBox())
            #print("Left bearing: ", F[GlyphName(CC)].left_side_bearing)
            #print("Right bearing: ", F[GlyphName(CC)].right_side_bearing)
            
            BB = F[GlyphName(CC)].boundingBox()
            
            # Shift X-position by the left bearing. I think there's nothing to
            # do here because everything is aligned to X=0 point
            
            X += 0
        
        
            L = F[GlyphName(CC)].layers[1]
            L.transform((1,0,0,1,X,0))
            L.draw(P)
            
            # Shift X-position by the right bearing. Here, we do actually use
            # it.
            
            X += BB[2] + F[GlyphName(CC)].right_side_bearing
            
            
            
            
        
        C.autoHint()
        P = None
    
    
    

    
    C = F.createChar(0xE08B, GlyphName(0xE08B))
    P = C.glyphPen()
    F["timeSigCommon"].draw(P)
    
    P.moveTo((DEFAULTS["cut_time"]["x"]-DEFAULTS["cut_time"]["thickness"]/2,DEFAULTS["cut_time"]["y1"]))
    P.lineTo((DEFAULTS["cut_time"]["x"]-DEFAULTS["cut_time"]["thickness"]/2,DEFAULTS["cut_time"]["y2"]))
    P.lineTo((DEFAULTS["cut_time"]["x"]+DEFAULTS["cut_time"]["thickness"]/2,DEFAULTS["cut_time"]["y2"]))
    P.lineTo((DEFAULTS["cut_time"]["x"]+DEFAULTS["cut_time"]["thickness"]/2,DEFAULTS["cut_time"]["y1"]))
    P.closePath()
    C.removeOverlap()


    C.left_side_bearing = 0
    C.right_side_bearing = 0
    C.autoHint()
    P = None
    

    
     
    """ + \
    """
    F.save("{0}")
    """.format(str(out_path))


    with open('s2.py', 'w') as f_scr:
        f_scr.write("DEFAULTS = {0}".format(str(DEFAULTS)))
        f_scr.write(textwrap.dedent(S))
    subprocess.run(['fontforge', '--script', 's2.py'])


    # Create a SMuFL metadata file


    S = ""
    S += """

    import json
    import fontforge

    D = {}

    """
    
    S += "\n    D.update({'fontName': " + '"{0}"'.format(__NAME__) + "})\n"
    S += "    D.update({'fontVersion': " + '"{0}"'.format(__VERSION__) + "})\n"

    S += """
    D.update({'engravingDefaults': {}})
    D.update({'glyphAdvanceWidths': {}})
    D.update({'glyphBBoxes': {}})
    D.update({'glyphsWithAnchors': {}})
    """

    S += """
    f = fontforge.open("{0}")
    """.format(str(out_path))

    S += """

    for GLIF in f.glyphs():
        D['glyphAdvanceWidths'].update({GLIF.glyphname: GLIF.width / 250.0})
        (xa, ya, xb, yb) = GLIF.boundingBox()
        D['glyphBBoxes'].update({GLIF.glyphname: {'bBoxNE': [xb/250.0, yb/250.0], 'bBoxSW': [xa/250.0, ya/250.0]}})
        if len(GLIF.anchorPoints) != 0:
            E = {}
            for ANCHOR in GLIF.anchorPoints:
                E.update({ANCHOR[0]: [ANCHOR[2]/250.0, ANCHOR[3]/250.0]})
            D['glyphsWithAnchors'].update({GLIF.glyphname: E})
    """

    S += """

    # Now the generic stuff

    D['engravingDefaults'].update({'textFontFamily': ['serif']})

    D['engravingDefaults'].update({'beamSpacing': DEFAULTS['beamSpacing']/250.0})
    D['engravingDefaults'].update({'beamThickness': DEFAULTS['beamThickness']/250.0})
    D['engravingDefaults'].update({'staffLineThickness': DEFAULTS['staffLineThickness']/250.0})
    D['engravingDefaults'].update({'stemThickness': DEFAULTS['stemThickness']/250.0})

        # "arrowShaftThickness":0.16,
        # "barlineSeparation":0.4,
        # "beamSpacing":0.25,
        # "beamThickness":0.5,
        # "bracketThickness":0.5,
        # "dashedBarlineDashLength":0.5,
        # "dashedBarlineGapLength":0.25,
        # "dashedBarlineThickness":0.16,
        # "hBarThickness":1.0,
        # "hairpinThickness":0.16,
        # "legerLineExtension":0.4,
        # "legerLineThickness":0.16,
        # "lyricLineThickness":0.16,
        # "octaveLineThickness":0.16,
        # "pedalLineThickness":0.16,
        # "repeatBarlineDotSeparation":0.16,
        # "repeatEndingLineThickness":0.16,
        # "slurEndpointThickness":0.1,
        # "slurMidpointThickness":0.22,
        # "staffLineThickness":0.13,
        # "stemThickness":0.12,
        # "subBracketThickness":0.16,
        # "textEnclosureThickness":0.16,
        # "thickBarlineThickness":0.5,
        # "thinBarlineThickness":0.16,
        # "tieEndpointThickness":0.1,
        # "tieMidpointThickness":0.22,
        # "tupletBracketThickness":0.16

    """

    out_metadata = out_path.parent.joinpath(out_path.stem + "-metadata.json")

    S += """

    with open("{0}", "w") as f:
        json.dump(D, f, indent = "\t")

    """.format(str(out_metadata))

    with open('s7.py', 'w') as f_scr:
        f_scr.write("DEFAULTS = {0}".format(str(DEFAULTS)))
        f_scr.write(textwrap.dedent(S))
    subprocess.run(['fontforge', '--script', 's7.py'])


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(-1)
    build_font(pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]))

