

# According to this thread:  https://musescore.org/en/node/306815
# the only way to add music fonts to musescore is to compile them in.
# Is that still the case?? Anyway, build it below to prove that it's possible.
#
# 

import pathlib
import os
import shutil
import subprocess
import sys
import warnings



if sys.platform != "linux":
    warnings.warn("This script is really only intended to use with linux. Don't expect much success on your system.")


P = pathlib.Path(__file__).parent.resolve()
print(P)

FULLY_REFRESHED = False


if P.joinpath("mscore_build").is_dir():
    if FULLY_REFRESHED:
        # Completely delete the tree
        shutil.rmtree(P.joinpath("mscore_build"), ignore_errors=True)
        os.mkdir(P.joinpath("mscore_build"))
    else:
        # Only delete build output
        shutil.rmtree(P.joinpath("mscore_build", "_build"), ignore_errors=True)
        shutil.rmtree(P.joinpath("mscore_build", "_install"), ignore_errors=True)
else:
    os.mkdir(P.joinpath("mscore_build"))
os.chdir(P.joinpath("mscore_build"))

TAG_DEFINITION = ["-b", "v3.6.2"]
subprocess.run(["git", "clone", "https://github.com/musescore/MuseScore", "T"] + TAG_DEFINITION)

os.chdir(P.joinpath("mscore_build", "T"))

os.mkdir(P.joinpath("mscore_build", "_build"))
os.mkdir(P.joinpath("mscore_build", "_install"))
os.chdir(P.joinpath("mscore_build", "_build"))

# Point to our install directory
CMAKE_OPTIONS = ["-DCMAKE_INSTALL_PREFIX={0}".format(str(pathlib.Path("..", "_install")))]
# Turn off a bunch of things we don't need
CMAKE_OPTIONS += ["-DBUILD_ALSA=OFF", "-DBUILD_JACK=OFF", "-DBUILD_LAME=ON", "-DBUILD_PORTAUDIO=OFF", "-DBUILD_PORTMIDI=OFF", "-DBUILD_PULSEAUDIO=OFF", "-DBUILD_TELEMETRY_MODULE=OFF", "-DUSE_SYSTEM_FREETYPE=OFF"]
subprocess.run(["cmake", str(pathlib.Path("..", "T"))] + CMAKE_OPTIONS)

subprocess.run(["cmake", "--build"])
subprocess.run(["cmake", "--build", ".", "--target", "install"])

# The following installations are needed on Ubuntu 22.04.1

#sudo apt-get install qtbase5-dev qttools5-dev qttools5-dev-tools qtwebengine5-dev qtscript5-dev libqt5xmlpatterns5-dev libqt5svg5-dev libqt5webkit5-dev
#sudo apt-get install qtquickcontrols2-5-dev libqt5networkauth5 libqt5networkauth5-dev
#sudo apt-get install libsndfile1-dev
#sudo apt-get install libqt5x11extras5 libqt5x11extras5-dev 
#sudo apt-get install qtbase5-private-dev
