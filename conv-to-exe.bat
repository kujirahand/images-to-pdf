pyinstaller images-to-pdf.py --onefile
copy README.md dist\README.txt
mkdir dist\pdf-in
copy pdf-in\test.heic dist\pdf-in\test.heic
pause
