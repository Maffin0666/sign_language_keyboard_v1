@echo off
echo ========================================
echo  Building Sign Language Keyboard
echo ========================================
pip install -r requirements.txt
pyinstaller --onefile --windowed --name "SignLanguageKeyboard" --icon=resources/icon.ico main.py
echo.
echo Build complete! Check dist/ folder.
pause