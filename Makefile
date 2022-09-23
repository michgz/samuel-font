
PYTHON = python

all: test_verovio samuel-12.sfd otf

otf: samuel-12.sfd src/build_otf.py _build
	$(PYTHON) src/build_otf.py

samuel-12.sfd: src/build_font.py
	$(PYTHON) src/build_font.py samuel-11.sfdir samuel-12.sfd

test_verovio: src/test_verovio.py samuel-12.sfd
	$(PYTHON) src/test_verovio.py samuel-12.sfd


.PHONY: test_verovio otf
