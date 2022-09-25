
FONT_NAME = Samuel
FONT_NAME_LOWCASE = $(shell python -c "print('$(FONT_NAME)'.lower())")

PYTHON = python
MKDIR = mkdir
RM = rm -fr
COPY = cp

all: test_pillow samuel-12.sfd

otf: samuel-12.sfd src/build_otf.py _build
	$(RM) _build/otf
	$(MKDIR) _build/otf
	$(PYTHON) src/build_otf.py samuel-12.sfd _build/otf/$(FONT_NAME_LOWCASE)-14.otf
	$(COPY) _build/otf/$(FONT_NAME_LOWCASE)-14.otf font/$(FONT_NAME_LOWCASE).otf

samuel-12.sfd: src/build_font.py samuel-11.sfdir
	$(PYTHON) src/build_font.py samuel-11.sfdir samuel-12.sfd

test_verovio: src/test_verovio.py samuel-12.sfd
	$(PYTHON) src/test_verovio.py samuel-12.sfd

test_pillow: otf
	$(PYTHON) src/test_pillow.py _build/otf/$(FONT_NAME_LOWCASE)-14.otf

_build:
	$(MKDIR) _build

.PHONY: test_verovio test_pillow otf
