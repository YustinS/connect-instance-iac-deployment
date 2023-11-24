BASE := $(shell /bin/pwd)
CODE_COVERAGE = 70

install:
	$(info [*] Validating pip install )
	@pip install --upgrade pip
	$(MAKE) dev

dev:
	$(info [*] Installing project dependencies)
	@pip install -r requirements.txt
	@pip install -r requirements-dev.txt

test:
	@pytest tests -vv