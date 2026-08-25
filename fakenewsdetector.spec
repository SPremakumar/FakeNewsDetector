from PyInstaller.utils.hooks import collect_all

# TensorFlow / Keras
datas = []
binaries = []
hiddenimports = []

for package in ["tensorflow", "keras"]:
    tmp_datas, tmp_binaries, tmp_hiddenimports = collect_all(package)

    datas += tmp_datas
    binaries += tmp_binaries
    hiddenimports += tmp_hiddenimports

# Fichiers du projet
datas += [
    ("backend/fake_news_model.keras", "backend"),
    ("backend/vocab.json", "backend"),
    ("frontend/dist", "frontend/dist"),
]

# Analyse
a = Analysis(
    ["launcher.py"],
    pathex=[".", "backend"],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    excludes=["tkinter"],
    noarchive=False,
)

# PYZ
pyz = PYZ(a.pure)

# EXE
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="FakeNewsDetector",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
)