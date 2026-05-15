@echo off
echo ============================================
echo   Сборка: Клавиатура нотаций РЖЯ
echo ============================================
echo.

REM Проверяем наличие Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ОШИБКА: Python не найден! Установите Python 3.8+ и добавьте в PATH.
    pause
    exit /b 1
)

REM Устанавливаем зависимости
echo [1/3] Установка зависимостей...
pip install PyQt5 pyinstaller pyperclip --quiet

REM Собираем
echo.
echo [2/3] Сборка EXE файла...
echo Это может занять несколько минут...
echo.

pyinstaller ^
    --onefile ^
    --windowed ^
    --name "SignLanguageKeyboard" ^
    --add-data "keyboard_data.py;." ^
    --add-data "theme_manager.py;." ^
    --add-data "custom_font.py;." ^
    --icon=NONE ^
    --clean ^
    --noconfirm ^
    main.py

echo.
if exist "dist\SignLanguageKeyboard.exe" (
    echo ============================================
    echo   УСПЕХ! Файл создан:
    echo   dist\SignLanguageKeyboard.exe
    echo ============================================
    echo.
    echo Размер файла:
    for %%A in ("dist\SignLanguageKeyboard.exe") do echo   %%~zA байт
    echo.
    echo Вы можете скопировать SignLanguageKeyboard.exe
    echo на любой компьютер с Windows и запустить.
    echo Установка не требуется!
) else (
    echo ОШИБКА: Файл не был создан.
    echo Проверьте логи выше.
)

echo.
pause