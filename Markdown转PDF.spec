# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all
import glob

datas = []
binaries = []
hiddenimports = []
tmp_ret = collect_all('weasyprint')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('markdown')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('pygments')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]

# WeasyPrint depends on the native GTK/Pango stack.  These DLLs are
# assembled by win-build/msys-packages/install_pango.py in the Wine prefix.
binaries += [(path, '.') for path in glob.glob(r'C:\md2pdf-dll\ucrt64\bin\*.dll')]


a = Analysis(
    ['Z:/home/javen03/data/md2pdf/Markdown转PDF_GUI/gui.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
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
    name='Markdown转PDF',
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
