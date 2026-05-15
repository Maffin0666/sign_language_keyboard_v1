# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['C:\\Users\\Masha\\PycharmProjects\\sign_language_keyboard\\main.py'],
    pathex=[],
    binaries=[],
    datas=[('keyboard_data.py', '.'), ('theme_manager.py', '.'), ('custom_font.py', '.')],
    hiddenimports=['keyboard_data', 'theme_manager', 'custom_font', 'PyQt5.sip'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='SignLanguageKeyboard',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
