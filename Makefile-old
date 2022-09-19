
# Installed using:
#     pip install fonttools
#
FONTTOOLS_TTX = fonttools ttx
RM = rm -rf
PYTHON = python
FONTFORGE = fontforge
CP = cp -f

clean:
	$(RM) test.pdf
	$(RM) ./samuel-*.otf
	$(RM) ~/.fonts/samuel-*.otf
	# Note: the following line needs "sudo" privileges.
	$(RM) /usr/local/lilypond/usr/share/lilypond/current/fonts/otf/samuel-*.otf

all:
	$(FONTFORGE) --lang=py -script make_for_lilypond.py
	$(CP) samuel-*.otf ~/.fonts
	# Note: the following line needs "sudo" privileges.
	$(CP) samuel-*.otf /usr/local/lilypond/usr/share/lilypond/current/fonts/otf
	lilypond -o test lp/test.ly
