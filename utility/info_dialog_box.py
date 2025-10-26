from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtGui import QIcon

class InfoDialogBox:
    def _show_dialog(title: str, text: str, type: QMessageBox, message: str=""):
        """Show an error dialog for any cleanup issue"""
        msg = QMessageBox()
        msg.setWindowIcon(QIcon("ico/info.ico"))
        msg.setIcon(type)
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setInformativeText(message)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()
