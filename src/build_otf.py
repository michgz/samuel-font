

import pathlib
import subprocess

# Delete any old file
pathlib.Path("..", "samuel-14.otf").unlink()


S = """
import fontforge

F = fontforge.open("../samuel-12.sfd")

F.generate("../samuel-14.otf")

"""

with open("s8.py", "w") as f8:
    f8.write(S)
    
subprocess.run(['fontforge', '--script', 's8.py'])


