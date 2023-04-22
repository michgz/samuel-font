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


__NAME__ = "Samuel"




def test_verovio(in_path):


    # Put the font into the verovio data directory.

    P = pathlib.Path(__file__).parent.joinpath("verovio_data")
    #P.mkdir(exist_ok =True)


    # Copy all files into the relevant directory
    shutil.copytree(in_path, P)



    # Run Verovio to render the test score
    import verovio

    V = verovio.toolkit()
    V.setResourcePath(str(P))
    V.loadFile('test1.musicxml')
    V.setFont("Samuel")   # use the font that we've just created
    V.renderToSVGFile('test1out.svg')


    # Change from SVG to PNG. There are surprisingly few cross-platform ways of doing this.
    # Reportlab.graphics.renderPM gives terrible results - don't use it! This method using
    # inkscape is okay, but it requires installing inkscape.



    P_IN = pathlib.Path.cwd().resolve().joinpath("test1out.svg")
    P_OUT = pathlib.Path.cwd().resolve().joinpath("test1out.png")

    subprocess.run(['inkscape', '-o', str(P_OUT), '--export-overwrite', '--export-type=png', '--export-area={0}:{1}:{2}:{3}'.format(0, 0, 1600, 500), '--export-background=white', str(P_IN)])


if __name__=="__main__":
  
  
    import argparse


    # Parse command-line parameters
    parser = argparse.ArgumentParser(description="USe the font in verovio")

    parser.add_argument("-i", "--indir", type=pathlib.Path, required=True)
    

    args = parser.parse_args()



    # Now call the main function
    test_verovio(args.indir)
