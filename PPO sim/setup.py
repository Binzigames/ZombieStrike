import sys
from cx_Freeze import setup, Executable
base = None
if sys.platform == "win32":
    base = "Win32GUI"


executables = [
    Executable("main.py", base=base, target_name="ZombieStrike.exe")
]


build_exe_options = {
    "packages": ["os"],
    "excludes": ["tkinter"],
}

setup(
    name="ZombieStrike",
    version="0.9",
    description="game made by porko team more here https://porko-dev.itch.io/zombie-strike",
    options={"build_exe": build_exe_options},
    executables=executables
)
