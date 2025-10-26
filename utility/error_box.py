from PyQt6.QtWidgets import QMessageBox

class ErrorHandle:
    def _show_error_dialog(message: str):
        """Show an error dialog for any cleanup issue"""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setWindowTitle("Error")
        msg.setText("An error occurred")
        msg.setInformativeText(message)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()
