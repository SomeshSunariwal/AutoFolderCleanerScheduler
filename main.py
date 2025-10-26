# main.py
import sys
import subprocess
import importlib

# -----------------------------
#  AUTO-INSTALL DEPENDENCIES
# -----------------------------
required_packages = [
    "PyQt6",
]

def install_package(package):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    except Exception as e:
        print(f"⚠️ Failed to install {package}: {e}")

def check_and_install():
    for package in required_packages:
        try:
            importlib.import_module(package)
        except ImportError:
            print(f"📦 Installing missing package: {package}")
            install_package(package)

check_and_install()

# -----------------------------
#  IMPORT AFTER DEP CHECK
# -----------------------------
from PyQt6.QtWidgets import QApplication
from ui.ui_main import MainWindow
from utility.storage import load_data, save_data

# -----------------------------
#  THEME HANDLER
# -----------------------------
def apply_theme(app, theme):
    if theme == "dark":
        app.setStyleSheet("""
            QWidget { background-color: #1e1e1e; color: #dddddd; }
            QPushButton { background-color: #333; color: #fff; padding: 5px; border-radius: 4px; }
            QPushButton:hover { background-color: #444; }
        """)
    else:
        app.setStyleSheet("")  # default light theme

# -----------------------------
#  MAIN APP ENTRY
# -----------------------------
def main():
    app = QApplication(sys.argv)
    data = load_data()
    apply_theme(app, data["settings"].get("theme", "light"))
    window = MainWindow(app, data)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
