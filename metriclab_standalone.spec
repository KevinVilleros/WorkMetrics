"""
PyInstaller Spec para MetricLab Standalone
Genera un .exe completo con Backend + Frontend + Database
"""

import os
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# ============================================================
# CONFIGURACIÓN
# ============================================================

block_cipher = None
app_name = 'MetricLab'
script = 'metriclab_complete.py'

# Recopilar datos de paquetes
django_datas = collect_data_files('django')
mediapipe_datas = collect_data_files('mediapipe')
frontend_build = [('frontend/build', 'frontend/build')]

# Dependencias escondidas
hidden_imports = [
    'django',
    'django.conf',
    'django.core',
    'django.db',
    'django.apps',
    'rest_framework',
    'corsheaders',
    'mediapipe',
    'cv2',
    'numpy',
    'PIL',
    'psycopg2',
]

# ============================================================
# ANÁLISIS
# ============================================================

a = Analysis(
    [script],
    pathex=[],
    binaries=[],
    datas=django_datas + mediapipe_datas + frontend_build,
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludedimports=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# ============================================================
# PYZ
# ============================================================

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# ============================================================
# EXE
# ============================================================

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name=app_name,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='frontend/public/favicon.ico' if os.path.exists('frontend/public/favicon.ico') else None,
)

# ============================================================
# COLECCIÓN
# ============================================================

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name=app_name,
)
