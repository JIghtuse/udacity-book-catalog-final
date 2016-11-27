#!/bin/bash

PROJECT_REPO=https://github.com/JIghtuse/udacity-book-catalog-final.git 
PROJECT_DIR=/var/www/catalog

mkdir -p "$PROJECT_DIR"
cd "$PROJECT_DIR" || exit

git clone "$PROJECT_REPO" "$PROJECT_DIR"

virtualenv venv
. "$PROJECT_DIR/venv/bin/activate"
pip3 install -r requirements.txt
python3 database_setup.py
python3 database_populate.py
deactivate
