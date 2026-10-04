# -*- coding: utf-8 -*-
"""
Clarity Lifetime v2.7 - Launcher
Entry point called from run.bat. Boots the loader UI defined in main.py
(Target FPS, Arduino, RP2040, Makou, GamePadEmu, AI Model) and hands
control to the aimbot once the user clicks Start.
"""
import os
import sys
import ctypes
import runpy
import traceback


def _ensure_admin():
    try:
        if ctypes.windll.shell32.IsUserAnAdmin():
            return
        params = " ".join(f'"{a}"' for a in sys.argv)
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, f'"{__file__}" {params}', None, 1
        )
        sys.exit(0)
    except Exception:
        pass


def _bootstrap():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)

    os.chdir(project_root)

    if script_dir not in sys.path:
        sys.path.insert(0, script_dir)
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

    configs_dir = os.path.join(project_root, "extra", "configs")
    if not os.path.isdir(configs_dir):
        os.makedirs(configs_dir, exist_ok=True)

    main_path = os.path.join(script_dir, "main.py")
    if not os.path.isfile(main_path):
        print(f"[Launcher] main.py not found at: {main_path}")
        input("Press Enter to exit...")
        sys.exit(1)

    try:
        ctypes.windll.kernel32.SetConsoleTitleW("Clarity Lifetime v2.7")
    except Exception:
        pass

    runpy.run_path(main_path, run_name="__main__")


if __name__ == "__main__":
    _ensure_admin()
    try:
        _bootstrap()
    except SystemExit:
        raise
    except Exception as e:
        print("[Launcher] Fatal error:", e)
        traceback.print_exc()
        input("Press Enter to exit...")
