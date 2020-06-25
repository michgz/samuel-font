
# Installed using:
#     pip install fonttools
#
FONTTOOLS_TTX = fonttools ttx

RM = rm -rf

# Initialise the source code from the master font 
init-src:
	$(RM) ./11.ttx ./13.ttx ./14.ttx ./16.ttx ./18.ttx ./20.ttx ./20.ttx ./23.ttx
	$(FONTTOOLS_TTX) -o ./11.ttx ./Example\ Lilypond/lilyboulez-master/otf/lilyboulez-11.otf
	$(FONTTOOLS_TTX) -o ./13.ttx ./Example\ Lilypond/lilyboulez-master/otf/lilyboulez-13.otf
	$(FONTTOOLS_TTX) -o ./14.ttx ./Example\ Lilypond/lilyboulez-master/otf/lilyboulez-14.otf
	$(FONTTOOLS_TTX) -o ./16.ttx ./Example\ Lilypond/lilyboulez-master/otf/lilyboulez-16.otf
	$(FONTTOOLS_TTX) -o ./18.ttx ./Example\ Lilypond/lilyboulez-master/otf/lilyboulez-18.otf
	$(FONTTOOLS_TTX) -o ./20.ttx ./Example\ Lilypond/lilyboulez-master/otf/lilyboulez-20.otf
	$(FONTTOOLS_TTX) -o ./23.ttx ./Example\ Lilypond/lilyboulez-master/otf/lilyboulez-23.otf
	$(FONTTOOLS_TTX) -o ./26.ttx ./Example\ Lilypond/lilyboulez-master/otf/lilyboulez-26.otf
	$(RM) *-LILC.bin *-LILF.bin *-LILY.bin
	# Now use a python script to extract the LILC, LILF, LILY tables. Results will have a .bin
	# extension, but should actually be ASCII text.
	python extract_tables.py 11
	python extract_tables.py 13
	python extract_tables.py 14
	python extract_tables.py 16
	python extract_tables.py 18
	python extract_tables.py 20
	python extract_tables.py 23
	python extract_tables.py 26

PYTHON = python

all:
	$(RM) ~/.fonts/lilyboulez-11.otf ~/.fonts/lilyboulez-13.otf ~/.fonts/lilyboulez-14.otf ~/.fonts/lilyboulez-16.otf ~/.fonts/lilyboulez-18.otf ~/.fonts/lilyboulez-20.otf ~/.fonts/lilyboulez-23.otf ~/.fonts/lilyboulez-26.otf 
	$(PYTHON) expand.py 11
	$(FONTTOOLS_TTX) -o ~/.fonts/lilyboulez-11.otf ./11-new.ttx
	$(PYTHON) expand.py 13
	$(FONTTOOLS_TTX) -o ~/.fonts/lilyboulez-13.otf ./13-new.ttx
	$(PYTHON) expand.py 14
	$(FONTTOOLS_TTX) -o ~/.fonts/lilyboulez-14.otf ./14-new.ttx
	$(PYTHON) expand.py 16
	$(FONTTOOLS_TTX) -o ~/.fonts/lilyboulez-16.otf ./16-new.ttx
	$(PYTHON) expand.py 18
	$(FONTTOOLS_TTX) -o ~/.fonts/lilyboulez-18.otf ./18-new.ttx
	$(PYTHON) expand.py 20
	$(FONTTOOLS_TTX) -o ~/.fonts/lilyboulez-20.otf ./20-new.ttx
	$(PYTHON) expand.py 23
	$(FONTTOOLS_TTX) -o ~/.fonts/lilyboulez-23.otf ./23-new.ttx
	$(PYTHON) expand.py 26
	$(FONTTOOLS_TTX) -o ~/.fonts/lilyboulez-26.otf ./26-new.ttx
	# Now actually use the new fonts to generate a PDF
	lilypond -o test lp/test.ly
