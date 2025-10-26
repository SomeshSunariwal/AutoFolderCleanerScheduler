# main.py
import sys
import subprocess
import importlib
from PyQt6.QtNetwork import QLocalServer, QLocalSocket
from PyQt6.QtWidgets import QApplication
from ui.ui_main import MainWindow
from utility.storage import load_data

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
#  SINGLE INSTANCE CHECK
# -----------------------------
server_instance = None  # global reference

def is_another_instance_running(app_id="WindowsAutoFolderCleaner"):
    global server_instance
    socket = QLocalSocket()
    socket.connectToServer(app_id)
    if socket.waitForConnected(500):
        print("⚠️ App is already running.")
        return True

    server_instance = QLocalServer()
    server_instance.listen(app_id)
    return False

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
    # Prevent multiple instances
    if is_another_instance_running():
        sys.exit(0)

    app = QApplication(sys.argv)
    data = load_data()
    apply_theme(app, data["settings"].get("theme", "light"))
    window = MainWindow(app, data)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()


# pyinstaller --clean --noconsole --onefile --icon=app.ico --add-data "ico;ico" main.py