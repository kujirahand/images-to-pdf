#!/bin/bash

PYTHON_BIN=/Library/Frameworks/Python.framework/Versions/3.11/bin
PYTHON=$PYTHON_BIN/python3
PYINSTALLER=$PYTHON_BIN/pyinstaller

ls $PYTHON_BIN/*
exit

$PYTHON -m pip install -r ./requirements.txt
$PYINSTALLER --onefile --noconsole ./images-to-pdf.py


