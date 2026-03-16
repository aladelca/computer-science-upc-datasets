VENV_PYTHON ?= .venv/bin/python
RAW_ROOT ?= data/raw
PROCESSED_ROOT ?= data/processed
LYRICS_TOP_N_TOKENS ?= 0

.PHONY: test build-course-dataset

test:
	.venv/bin/pytest

build-course-dataset:
	$(VENV_PYTHON) -m pachamix_data.cli build-course-dataset \
		--raw-root $(RAW_ROOT) \
		--processed-root $(PROCESSED_ROOT) \
		--lyrics-top-n-tokens $(LYRICS_TOP_N_TOKENS)
