#!/bin/bash

PYTHON_BIN=/Library/Frameworks/Python.framework/Versions/3.11/bin
PYTHON=$PYTHON_BIN/python3.11
PYINSTALLER=$PYTHON_BIN/pyinstaller

$PYTHON -m pip install -r requirements.txt
$PYINSTALLER --onefile images-to-pdf.py
