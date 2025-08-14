# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['C:\\Users\\sabaa\\Downloads\\horaryelectr1-main\\horary78-main\\backend\\app.py'],
    pathex=[],
    binaries=[],
    datas=[('C:\\Users\\sabaa\\Downloads\\horaryelectr1-main\\horary78-main\\backend\\horary_constants.yaml', '.'), ('C:\\Users\\sabaa\\Downloads\\horaryelectr1-main\\horary78-main\\backend\\horary_config.py', '.'), ('C:\\Users\\sabaa\\Downloads\\horaryelectr1-main\\horary78-main\\backend\\production_server.py', '.')],
    hiddenimports=['swisseph', 'timezonefinder', 'geopy', 'pytz', 'flask', 'flask_cors'],
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
    name='horary_backend',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
