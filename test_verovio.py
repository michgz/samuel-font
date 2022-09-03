# Try using the font with the "Verovio" library


import pathlib
import venv
import os
import sys


P = pathlib.Path(venv.sysconfig.get_path('platlib'))

if not P.joinpath('verovio').is_dir():
    print('Could not find verovio installed in this virtual environment. Try:\n\n    pip install verovio\n')
    sys.exit(-1)



if not os.access(P.joinpath('verovio'), os.W_OK):
    print('Do not have write access to the verovio installation. Most likely you are running\nfrom the main installation of python rather than a virtual environment.\nPlease call this script from a virutal environment. See:\n\n    https://docs.python.org/3/library/venv.html\n')
    sys.exit(-1)



# Run Verovio to render the test score
import verovio

V = verovio.toolkit()
V.loadFile('test1.musicxml')
V.setFont('Petaluma')
V.renderToSVGFile('test1out.svg')


# Change from SVG to PNG. There are surprisingly few cross-platform ways of doing this.
# Reportlib.graphics.renderPM gives terrible results - don't use it! This method using
# inkscape is okay, but it requires installing inkscape.


import subprocess

P_IN = pathlib.Path.cwd().resolve().joinpath("test1out.svg")
P_OUT = pathlib.Path.cwd().resolve().joinpath("test1out.png")

subprocess.run(['inkscape', '-o', str(P_OUT), '--export-overwrite', '--export-type=png', '--export-area={0}:{1}:{2}:{3}'.format(0, 0, 1000, 500), '--export-background=white', str(P_IN)])

