
FONT_NAME = Samuel


# Define some basic commands
PYTHON = python
FONTFORGE = fontforge
MKDIR = mkdir -p
RM = rm -fr
COPY = cp

# Working directories
BUILD_DIR   = _build
TMP_DIR     = _build/tmp


FONT_NAME_LOWCASE = $(shell $(PYTHON) -c "print('$(FONT_NAME)'.lower())")


all: test_pillow $(TMP_DIR)/$(FONT_NAME_LOWCASE)-12.sfd

otf: $(TMP_DIR)/$(FONT_NAME_LOWCASE)-12.sfd src/build_otf.py $(BUILD_DIR) $(TMP_DIR)
	$(RM)     $(BUILD_DIR)/otf
	$(MKDIR)  $(BUILD_DIR)/otf
	$(FONTFORGE) --script src/build_otf.py                      \
            --in $(TMP_DIR)/$(FONT_NAME_LOWCASE)-12.sfd         \
            --out _build/otf/$(FONT_NAME_LOWCASE)-14.otf        
	$(COPY)   $(TMP_DIR)/$(FONT_NAME_LOWCASE)-12-metadata.json _build/otf/$(FONT_NAME_LOWCASE)-metadata.json
	$(COPY)   $(BUILD_DIR)/otf/$(FONT_NAME_LOWCASE)-14.otf font/$(FONT_NAME_LOWCASE).otf
	$(COPY)   $(BUILD_DIR)/otf/$(FONT_NAME_LOWCASE)-metadata.json font/

$(TMP_DIR)/$(FONT_NAME_LOWCASE)-12.sfd: _check_requirements $(TMP_DIR) src/build_font.py $(FONT_NAME_LOWCASE)-11.sfdir
	$(FONTFORGE) --script src/build_font.py                     \
             --in $(FONT_NAME_LOWCASE)-11.sfdir                 \
             --out $(TMP_DIR)/$(FONT_NAME_LOWCASE)-12.sfd       \
             --defaults src/my_defaults.py                      \
             --metadata-out $(TMP_DIR)/$(FONT_NAME_LOWCASE)-12-metadata.json

test_verovio: src/test_verovio.py $(TMP_DIR)/$(FONT_NAME_LOWCASE)-12.sfd
	$(PYTHON) src/test_verovio.py $(TMP_DIR)/$(FONT_NAME_LOWCASE)-12.sfd

test_pillow: otf
	$(PYTHON) src/test_pillow.py _build/otf/$(FONT_NAME_LOWCASE)-14.otf

_build:
	$(MKDIR) _build

_build/tmp: _build
	$(MKDIR) _build/tmp

_check_requirements: _build
	$(PYTHON) src/check_requirements.py > _build/RequirementsCheck.txt

clean:
	$(RM) _build/tmp

.PHONY: test_verovio test_pillow otf clean _check_requirements
