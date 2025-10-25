# ui_settings.py
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QComboBox, QPushButton, QHBoxLayout
)
from PyQt6.QtCore import Qt, QSize

class SettingsDialog(QDialog):
    def __init__(self, current_theme="light", parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setFixedSize(QSize(320, 160))  # ✅ Fixed dialog width & height
        self.theme = current_theme
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Label
        label = QLabel("Select Theme:")
        label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(label)

        # Combo Box
        self.cmb_theme = QComboBox()
        self.cmb_theme.addItems(["light", "dark"])
        self.cmb_theme.setCurrentText(self.theme)
        self.cmb_theme.setFixedWidth(180)  # ✅ Fix width to avoid shrink
        layout.addWidget(self.cmb_theme, alignment=Qt.AlignmentFlag.AlignLeft)

        # Buttons
        btns = QHBoxLayout()
        self.btn_save = QPushButton("Save")
        self.btn_cancel = QPushButton("Cancel")

        self.btn_save.setFixedWidth(100)
        self.btn_cancel.setFixedWidth(100)

        self.btn_cancel.clicked.connect(self.reject)
        self.btn_save.clicked.connect(self.accept)

        btns.addWidget(self.btn_save)
        btns.addWidget(self.btn_cancel)
        layout.addLayout(btns)

        self.setLayout(layout)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)