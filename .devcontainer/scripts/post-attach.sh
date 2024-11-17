#!/bin/bash

poetry install
poetry export -f requirements.txt -o requirements.txt --without-hashes

poetry run flet run -r -d --web --port 8000 app