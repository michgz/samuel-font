
FONT_NAME = Samuel
FONT_NAME_LOWCASE = $(shell python -c "print('$(FONT_NAME)'.lower())")

PYTHON = python
MKDIR = mkdir
RM = rm -fr
COPY = cp

all: test_samantha samantha-12.sfd

otf: samuel-12.sfd src/build_otf.py _build
	$(RM) _build/otf
	$(MKDIR) _build/otf
	$(PYTHON) src/build_otf.py samuel-12.sfd _build/otf/$(FONT_NAME_LOWCASE)-14.otf
	$(COPY) samuel-12-metadata.json _build/otf/$(FONT_NAME_LOWCASE)-metadata.json
	$(COPY) _build/otf/$(FONT_NAME_LOWCASE)-14.otf font/$(FONT_NAME_LOWCASE).otf
	$(COPY) _build/otf/$(FONT_NAME_LOWCASE)-metadata.json font/

samantha-12.sfd: src/build_font.py samantha-11.sfdir
	$(PYTHON) src/build_font.py samantha-11.sfdir samantha-12.sfd

samuel-12.sfd: src/build_font.py samuel-11.sfdir
	$(PYTHON) src/build_font.py samuel-11.sfdir samuel-12.sfd

test_verovio: src/test_verovio.py samuel-12.sfd
	$(PYTHON) src/test_verovio.py samuel-12.sfd

test_samantha: src/test_samantha.py samantha-12.sfd
	$(PYTHON) src/test_samantha.py samantha-12.sfd

test_pillow: otf
	$(PYTHON) src/test_pillow.py _build/otf/$(FONT_NAME_LOWCASE)-14.otf

otf_samantha: samantha-12.sfd src/build_otf.py _build
	$(RM) _build/otf
	$(MKDIR) _build/otf
	$(PYTHON) src/build_otf.py samantha-12.sfd _build/otf/Samantha-14.otf

test_pillow_samantha: otf_samantha
	$(PYTHON) src/test_pillow.py _build/otf/Samantha-14.otf

_build:
	$(MKDIR) _build

.PHONY: test_verovio test_pillow test_samantha otf
