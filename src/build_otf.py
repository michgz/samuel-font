

import pathlib
import subprocess
import sys
import textwrap

def build_otf(in_sfd, out_otf):

    # Delete any old file
    try:
        out_otf.unlink()
    except FileNotFoundError:
        pass


    S = """
    import fontforge

    F = fontforge.open("{0}")

    F.generate("{1}")

    """.format(in_sfd.resolve(), out_otf.resolve())

    with open("s8.py", "w") as f8:
        f8.write(textwrap.dedent(S))
        
    subprocess.run(['fontforge', '--script', 's8.py'])


if __name__=="__main__":
    if len(sys.argv) < 3:
        sys.exit(-1)
    build_otf(pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]))

