"""
Check the build requirements
"""

import sys
import subprocess


# Output the python version
print(sys.version)
print(sys.platform)
print(sys.implementation)

# Check fontforge is installed
try:
    P = subprocess.Popen(['fontforge', '-c', 'import fontforge; print(fontforge.version())'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    outs, _ = P.communicate(timeout=15)
    print(outs.decode('utf-8').strip())  # Version of fontforge
except:
    print("Fontforge not installed")
    print(sys.exc_info())
    
    sys.exit(-1)

# All is okay!
sys.exit(0)
