# -*- coding: utf-8 -*-
"""
Скрипт сборки с дополнительными настройками.
Запуск: python build_spec.py
"""

import subprocess
import sys
import os


def build():
    """Собирает EXE файл."""

    # Убеждаемся что зависимости установлены
    print("Установка зависимостей...")
    subprocess.check_call([sys.executable, "-m", "pip", "install",
                           "PyQt5", "pyinstaller", "-q"])

    # Определяем путь к текущей директории
    script_dir = os.path.dirname(os.path.abspath(__file__))
    main_script = os.path.join(script_dir, "main.py")

    # Формируем команду PyInstaller
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",  # Один файл
        "--windowed",  # Без консоли
        "--name", "SignLanguageKeyboard",
        "--clean",  # Чистая сборка
        "--noconfirm",  # Без подтверждений

        # Включаем модули
        "--hidden-import", "keyboard_data",
        "--hidden-import", "theme_manager",
        "--hidden-import", "custom_font",
        "--hidden-import", "PyQt5.sip",

        # Добавляем файлы данных
        "--add-data", f"keyboard_data.py{os.pathsep}.",
        "--add-data", f"theme_manager.py{os.pathsep}.",
        "--add-data", f"custom_font.py{os.pathsep}.",

        main_script
    ]

    print("Сборка EXE...")
    print(" ".join(cmd))

    result = subprocess.run(cmd, cwd=script_dir)

    if result.returncode == 0:
        exe_path = os.path.join(script_dir, "dist", "SignLanguageKeyboard.exe")
        if os.path.exists(exe_path):
            size_mb = os.path.getsize(exe_path) / (1024 * 1024)
            print(f"\n{'=' * 50}")
            print(f"УСПЕХ! Создан: {exe_path}")
            print(f"Размер: {size_mb:.1f} МБ")
            print(f"{'=' * 50}")
        else:
            print("Файл не найден после сборки!")
    else:
        print(f"Ошибка сборки! Код: {result.returncode}")


if __name__ == "__main__":
    build()