from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtGui import QIcon
import os

class InfoDialogBox():

    def resource_path(self, relative_path):
        """Get absolute path to resource (works for dev & for PyInstaller .exe)"""
        try:
            # When running as .exe
            base_path = sys._MEIPASS
        except Exception:
            # When running as script
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)
        
    def _show_dialog(self, title: str, text: str, type: QMessageBox, message: str=""):
        """Show an error dialog for any cleanup issue"""
        msg = QMessageBox()
        msg.setWindowIcon(QIcon(self.resource_path("ico/main.ico")))
        msg.setIcon(type)
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setInformativeText(message)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()
