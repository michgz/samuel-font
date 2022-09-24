
PYTHON = python
MKDIR = mkdir

all: test_verovio samuel-12.sfd

otf: samuel-12.sfd src/build_otf.py _build
	$(MKDIR) _build/otf
	$(PYTHON) src/build_otf.py samuel-12.sfd _build/otf/samuel-14.otf

samuel-12.sfd: src/build_font.py
	$(PYTHON) src/build_font.py samuel-11.sfdir samuel-12.sfd

test_verovio: src/test_verovio.py samuel-12.sfd
	$(PYTHON) src/test_verovio.py samuel-12.sfd

_build:
	$(MKDIR) _build

.PHONY: test_verovio otf
