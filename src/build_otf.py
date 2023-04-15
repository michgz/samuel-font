"""
Output the OTF file
"""

import pathlib



def build_generate_otf(__INPUT_PATH__ : pathlib.Path, __OUTPUT_PATH__ : pathlib.Path):

    # Delete any old file
    try:
        __OUTPUT_PATH__.unlink()
    except FileNotFoundError:
        pass

    import fontforge

    F = fontforge.open(str(__INPUT_PATH__))

    F.generate(str(__OUTPUT_PATH__))




if __name__=="__main__":

    import argparse


    # Parse command-line parameters
    parser = argparse.ArgumentParser(description="Generate the OTF file")

    parser.add_argument("-i", "--in", type=pathlib.Path, required=True, dest="_in")
    parser.add_argument("-o", "--out", type=pathlib.Path, required=True)
    

    args = parser.parse_args()


    # Now call the main function
    build_generate_otf(args._in, args.out)


