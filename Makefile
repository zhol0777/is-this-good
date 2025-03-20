venv:
	uv venv

source:
	source .venv/bin/activate

requirements:
	uv pip install -r requirements.txt

build:
	python3 scripts/build_map.py