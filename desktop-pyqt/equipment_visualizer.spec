# -*- mode: python ; coding: utf-8 -*-

"""
PyInstaller Specification File for Equipment Visualizer Desktop App

WHAT: Configuration file for building .exe
WHY: Controls how PyInstaller packages your Python app into .exe
HOW: Specifies files, dependencies, and executable settings

ELI5: This is like a recipe telling PyInstaller how to cook your .exe file
"""

block_cipher = None

a = Analysis(
    ['main.py'],                           # Main Python file
    pathex=[],                             # Additional paths
    binaries=[],                           # Binary files (none needed)
    datas=[('config.ini', '.')],          # Include config.ini in .exe
    hiddenimports=[                        # Packages PyInstaller might miss
        'matplotlib.backends.backend_qt5agg',
        'PyQt5',
        'PyQt5.QtCore',
        'PyQt5.QtGui',
        'PyQt5.QtWidgets',
        'requests',
        'configparser',
    ],
    hookspath=[],                          # Custom hooks (none needed)
    hooksconfig={},
    runtime_hooks=[],                      # Runtime hooks (none needed)
    excludes=[],                           # Packages to exclude
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='EquipmentVisualizer',            # Name of .exe file
    debug=False,                           # Set to True for debugging
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,                              # Compress executable (smaller size)
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,                         # Don't show console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None                              # No icon for now
)
