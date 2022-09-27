

# According to this thread:  https://musescore.org/en/node/306815
# the only way to add music fonts to musescore is to compile them in.
# Is that still the case??
#
# 

import pathlib
import os
import shutil
import subprocess



P = pathlib.Path(__file__).parent.resolve()
print(P)

shutil.rmtree(P.joinpath("mscore_build"), ignore_errors=True)

os.mkdir(P.joinpath("mscore_build"))
os.chdir(P.joinpath("mscore_build"))

subprocess.run(["git", "clone", "https://github.com/musescore/MuseScore", "T"])

os.chdir(P.joinpath("mscore_build", "T"))

os.mkdir(P.joinpath("mscore_build", "T", "_build"))
os.mkdir(P.joinpath("mscore_build", "T", "_install"))
os.chdir(P.joinpath("mscore_build", "T", "_build"))
subprocess.run(["cmake", "..", "-DCMAKE_INSTALL_PREFIX=_install"])
subprocess.run(["cmake", "--build"])
subprocess.run(["cmake", "--build", ".", "--target", "install"])


#sudo apt-get install qtbase5-dev qttools5-dev qttools5-dev-tools qtwebengine5-dev qtscript5-dev libqt5xmlpatterns5-dev libqt5svg5-dev libqt5webkit5-dev
#sudo apt-get install qtquickcontrols2-5-dev libqt5networkauth5 libqt5networkauth5-dev
