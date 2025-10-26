from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QSpinBox,
    QComboBox, QPushButton, QCheckBox, QFileDialog, QMessageBox
)
from PyQt6.QtGui import QIcon
import os

class AddEditDialog(QDialog):
    def __init__(self, folder_data=None, parent=None):
        """
        folder_data: optional dict with existing values for editing
        """
        super().__init__(parent)
        self.setWindowTitle("Add / Edit Folder Schedule")
        self.setFixedSize(420, 380)
        self.setWindowIcon(QIcon(os.path.join("ico", "edit.ico")))
        # Ensure folder_data is always a dict
        self.folder_data = folder_data or {}  
        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        # Folder selection
        layout.addWidget(QLabel("Select Folder:"))
        folder_layout = QHBoxLayout()
        self.txt_folder = QLineEdit()
        self.txt_folder.setReadOnly(True)  
        self.txt_folder.textChanged.connect(lambda text: self.txt_folder.setToolTip(text))
        self.btn_browse = QPushButton("Browse")
        self.btn_browse.clicked.connect(self.browse_folder)
        folder_layout.addWidget(self.txt_folder)
        folder_layout.addWidget(self.btn_browse)
        layout.addLayout(folder_layout)

        # Interval
        layout.addWidget(QLabel("Delete Interval:"))
        interval_layout = QHBoxLayout()
        self.spn_interval = QSpinBox()
        self.spn_interval.setRange(1, 9999)
        self.cmb_interval = QComboBox()
        self.cmb_interval.addItems(["seconds", "minutes", "hours", "days"])
        interval_layout.addWidget(self.spn_interval)
        interval_layout.addWidget(self.cmb_interval)
        layout.addLayout(interval_layout)

        # Delete only files older than X
        layout.addWidget(QLabel("Delete only files older than:"))
        older_layout = QHBoxLayout()
        self.spn_older = QSpinBox()
        self.spn_older.setRange(0, 9999)
        self.cmb_older = QComboBox()
        self.cmb_older.addItems(["hours", "days"])
        older_layout.addWidget(self.spn_older)
        older_layout.addWidget(self.cmb_older)
        layout.addLayout(older_layout)

        # Options layout: Include Subfolders + Active/Disabled
        options_layout = QHBoxLayout()
        self.chk_sub = QCheckBox("Include Subfolders")
        self.chk_sub.setChecked(True)
        options_layout.addWidget(self.chk_sub)

        self.chk_status = QCheckBox("Active")
        self.chk_status.setChecked(True)
        options_layout.addWidget(self.chk_status)
        layout.addLayout(options_layout)

        self.run_status = False

        # Buttons
        btn_layout = QHBoxLayout()
        self.btn_save = QPushButton("Save")
        self.btn_cancel = QPushButton("Cancel")
        self.btn_save.clicked.connect(self.save_and_close)
        self.btn_cancel.clicked.connect(self.reject)
        btn_layout.addWidget(self.btn_save)
        btn_layout.addWidget(self.btn_cancel)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def load_data(self):
        """Load existing folder data if editing"""
        if not self.folder_data:
            return
        self.txt_folder.setText(self.folder_data.get("path", ""))
        self.spn_interval.setValue(self.folder_data.get("interval_value", 1))
        self.cmb_interval.setCurrentText(self.folder_data.get("interval_unit", "minutes"))
        self.spn_older.setValue(self.folder_data.get("older_than_value", 0))
        self.cmb_older.setCurrentText(self.folder_data.get("older_than_unit", "days"))
        self.chk_sub.setChecked(self.folder_data.get("include_subfolders", True))
        self.chk_status.setChecked(self.folder_data.get("active", True))
        self.run_status = self.folder_data.get("running", False)

    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.txt_folder.setText(folder)

    def save_and_close(self):
        """Validate and close the dialog if all required info is provided."""
        if not self.txt_folder.text().strip():
            QMessageBox.warning(self, "Error", "Please select a folder first!")
            return
        self.accept()  # Close dialog and return Accepted

    def get_data(self):
        """Return all input values as a dictionary"""
        return {
            "path": self.txt_folder.text(),
            "interval_value": self.spn_interval.value(),
            "interval_unit": self.cmb_interval.currentText(),
            "older_than_value": self.spn_older.value(),
            "older_than_unit": self.cmb_older.currentText(),
            "include_subfolders": self.chk_sub.isChecked(),
            "active": self.chk_status.isChecked(),
            "running": self.run_status
        }
