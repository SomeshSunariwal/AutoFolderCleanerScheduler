from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QSpinBox,
    QComboBox, QPushButton, QCheckBox, QFileDialog
)
from PyQt6.QtCore import Qt

class AddEditDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add / Edit Folder Schedule")
        self.setFixedSize(420, 380)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        # Folder selection
        layout.addWidget(QLabel("Select Folder:"))
        folder_layout = QHBoxLayout()
        self.txt_folder = QLineEdit()
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

        # Include Subfolders & Status
        options_layout = QHBoxLayout()
        
        # Include Subfolders checkbox
        self.chk_sub = QCheckBox("Include Subfolders")
        self.chk_sub.setTristate(False)  # Ensure only two states: checked/unchecked
        self.chk_sub.setChecked(True)    # Default ticked
        options_layout.addWidget(self.chk_sub)
        
        # Status checkbox (Active / Disabled)
        self.chk_status = QCheckBox("Active")
        self.chk_status.setTristate(False)
        self.chk_status.setChecked(True)  # Default Active
        options_layout.addWidget(self.chk_status)

        layout.addLayout(options_layout)

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

    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.txt_folder.setText(folder)

    def save_and_close(self):
        """Validate and close the dialog if all required info is provided."""
        if not self.txt_folder.text().strip():
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.warning(self, "Error", "Please select a folder first!")
            return
        self.accept()
