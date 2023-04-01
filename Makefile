
FONT_NAME = Samuel


# Define some basic commands
PYTHON = python
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
	$(PYTHON) src/build_otf.py $(TMP_DIR)/$(FONT_NAME_LOWCASE)-12.sfd _build/otf/$(FONT_NAME_LOWCASE)-14.otf
	$(COPY)   $(TMP_DIR)/samuel-12-metadata.json _build/otf/$(FONT_NAME_LOWCASE)-metadata.json
	$(COPY)   $(BUILD_DIR)/otf/$(FONT_NAME_LOWCASE)-14.otf font/$(FONT_NAME_LOWCASE).otf
	$(COPY)   $(BUILD_DIR)/otf/$(FONT_NAME_LOWCASE)-metadata.json font/

$(TMP_DIR)/$(FONT_NAME_LOWCASE)-12.sfd: _check_requirements $(TMP_DIR) src/build_font.py $(FONT_NAME_LOWCASE)-11.sfdir
	$(PYTHON) src/build_font.py $(FONT_NAME_LOWCASE)-11.sfdir $(TMP_DIR)/$(FONT_NAME_LOWCASE)-12.sfd

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
