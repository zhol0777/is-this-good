venv:
	uv venv

source:
	source .venv/bin/activate

requirements:
	uv pip install -r requirements.txt

build:
	sips -Z 700 images/map/*.jpg
	sips -Z 700 images/map/*.png
	python3 scripts/build_map.py