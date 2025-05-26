VENV := venv
PYTHON := $(VENV)/bin/python3
PIP := $(VENV)/bin/pip

.PHONY: run install clean

run: install
	$(PYTHON) main.py

install: check-graphviz
	@test -d $(VENV) || python3 -m venv $(VENV)
	$(PIP) install -r requirements.txt

check-graphviz:
	@which dot >/dev/null 2>&1 || { \
		echo "Graphviz não está instalado. Instalando..."; \
		sudo apt update && sudo apt install -y graphviz; \
	}

clean:
	rm -rf $(VENV)
	find . -type d -name "__pycache__" -exec rm -rf {} +