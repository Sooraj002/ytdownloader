# -*- mode: python ; coding: utf-8 -*-
import os
from PyInstaller.utils.hooks import collect_dynamic_libs

block_cipher = None

# Get the absolute path to FFmpeg files
ffmpeg_files = [
    ('ffmpeg/ffmpeg.exe', 'ffmpeg'),
    ('ffmpeg/ffprobe.exe', 'ffmpeg')
]

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=ffmpeg_files,
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# Add FFmpeg files to the bundle
a.binaries += ffmpeg_files

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='YouTubeDownloader',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=os.path.abspath('icon.ico') if os.path.exists('icon.ico') else None
) 