# ui_main.py
import os
import shutil
from PyQt6.QtWidgets import (
    QMainWindow, 
    QWidget, 
    QVBoxLayout, 
    QHBoxLayout, 
    QPushButton,
    QTableWidget, 
    QTableWidgetItem, 
    QHeaderView, 
    QMessageBox
)
from PyQt6.QtCore import Qt
from ui.ui_add_edit import AddEditDialog
from ui.ui_settings import SettingsDialog
from utility.storage import save_data
from PyQt6.QtWidgets import QMessageBox
from handler.task_handler import TaskHandler
from utility.status import StatusBar


class MainWindow(QMainWindow):
    def __init__(self, app_ref, data):
        super().__init__()
        self.app_ref = app_ref
        self.data = data
        self.setWindowTitle("AutoClean Scheduler")
        self.setFixedSize(1200, 700)
        # self.setMinimumSize(1200, 700)
        # self.setMaximumSize(1200, 700)

        # ✅ Create StatusBar instance here
        self.status_ui = StatusBar(self)
        
        # ✅ Create TaskScheduler instance here
        self.task = TaskHandler(self)

        # Initialize UI
        self.setup_ui()
        
    def setup_ui(self):
        button_height = 40  # desired height in pixels
        central = QWidget()
        layout = QVBoxLayout()

        # ---------------- Top buttons ----------------
        top_layout = QHBoxLayout()
        top_layout.addStretch()  # push the button to the right

        # Big toggle button
        self.btn_schedule = QPushButton("Schedule All")
        self.btn_schedule.setFixedSize(120, 50)  # big button
        self.btn_schedule.setStyleSheet("background-color: #0098FF; font-weight: bold; font-size: 15px; border-radius: 25px;")
        self.btn_schedule.setCheckable(True)  # allow toggle
        self.btn_schedule.clicked.connect(
            lambda checked: self.task.toggle_schedule(self.btn_schedule, checked)
        )

        top_layout.addWidget(self.btn_schedule)
        layout.addLayout(top_layout)  # add above table

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(
            ["Folder Path", "Schedule", "Status", "Edit", "Delete", "Run"]
        )
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.table)

        # Buttons
        btn_layout = QHBoxLayout()
        self.btn_add = QPushButton("➕ Add Folder")
        self.btn_add.setFixedHeight(button_height)
        self.btn_instant = QPushButton("⚡ Instant")
        self.btn_instant.setFixedHeight(button_height)   # NEW
        self.btn_settings = QPushButton("⚙️ Settings")
        self.btn_settings.setFixedHeight(button_height)
        self.btn_exit = QPushButton("❌ Exit")
        self.btn_exit.setFixedHeight(button_height)
        btn_layout.addWidget(self.btn_add)
        btn_layout.addWidget(self.btn_instant)  # add button to layout
        btn_layout.addWidget(self.btn_settings)
        btn_layout.addWidget(self.btn_exit)
        layout.addLayout(btn_layout)

        central.setLayout(layout)
        self.setCentralWidget(central)

        # signals
        self.btn_add.clicked.connect(self.add_folder)
        self.btn_instant.clicked.connect(self.instant_delete)
        self.btn_settings.clicked.connect(self.open_settings)
        self.btn_exit.clicked.connect(self.close)

        self.populate_table()
        self.status_ui.update_status("Ready!", "#22C55E")

    # -----------------------------
    # Populate the table
    # -----------------------------
    def populate_table(self):
        self.table.setRowCount(0)
        row_height = 40
        for i, folder in enumerate(self.data.get("folders", [])):
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setRowHeight(row, row_height)  # <-- Set row height here

            # Folder Path
            item = QTableWidgetItem(folder["path"])
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            item.setToolTip(folder["path"])
            self.table.setItem(row, 0, item)

            # Schedule
            interval = f'Every {folder["interval_value"]} {folder["interval_unit"]}'
            interval_item = QTableWidgetItem(interval)
            interval_item.setFlags(interval_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            interval_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 1, interval_item)

            # Status
            status_item = QTableWidgetItem("Active" if folder["active"] else "Paused")
            status_item.setFlags(status_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            status_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 2, status_item)

            # Edit Button
            edit_btn = QPushButton("✏️")
            edit_btn.clicked.connect(lambda _, r=row: self.edit_folder(r))
            self.table.setCellWidget(row, 3, edit_btn)

            # Delete Button
            del_btn = QPushButton("🗑️")
            del_btn.clicked.connect(lambda _, r=row: self.delete_folder(r))
            self.table.setCellWidget(row, 4, del_btn)

            # Play/Pause Button
            run_btn = QPushButton("▶️")  # Start with Play symbol
            run_btn.setCheckable(True)   # Toggle between Play/Pause
            
            run_btn.clicked.connect(
                lambda checked, r=row: self.task.toggle_run(self.data["folders"][r], self.table.cellWidget(r, 5), checked)
            )
            self.table.setCellWidget(row, 5, run_btn)

    # -----------------------------
    # Add Folder
    # -----------------------------
    def add_folder(self):
        dlg = AddEditDialog(parent=self)
        if dlg.exec():  # User clicked Save
            folder_data = dlg.get_data()  # Get all input values including active
            self.data["folders"].append(folder_data)
            save_data(self.data)
            self.populate_table()  # Refresh dashboard

    # -----------------------------
    # Edit Folder
    # -----------------------------
    def edit_folder(self, row):
        folder = self.data["folders"][row]
        self.task.pause_task(self.data["folders"][row])
        dlg = AddEditDialog(folder_data=folder, parent=self)  # Preload all values
        if dlg.exec():
            updated_data = dlg.get_data()  # Read updated values including status
            self.data["folders"][row] = updated_data
            save_data(self.data)
            self.populate_table()  # Refresh dashboard

    # -----------------------------
    # Delete Folder
    # -----------------------------
    def delete_folder(self, row):
        reply = QMessageBox.question(self, "Delete Folder",
            "Are you sure you want to delete this schedule?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.data["folders"].pop(row)
            save_data(self.data)
            self.populate_table()

    # -----------------------------
    # Settings
    # -----------------------------
    def open_settings(self):
        current_theme = self.data["settings"].get("theme", "light")
        dlg = SettingsDialog(current_theme, self)
        if dlg.exec():
            selected = dlg.cmb_theme.currentText()
            self.data["settings"]["theme"] = selected
            save_data(self.data)
            from main import apply_theme
            apply_theme(self.app_ref, selected)

            
    def instant_delete(self):
        """
        Delete all files and subfolders in folders that are Active immediately.
        """
        reply = QMessageBox.question(
            self, "Instant Delete",
            "Are you sure you want to delete ALL files and folders in all Active folders?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply != QMessageBox.StandardButton.Yes:
            return

        for folder in self.data.get("folders", []):
            if folder.get("active", True):  # Only active folders
                folder_path = folder.get("path")
                include_sub = folder.get("include_subfolders", True)
                if folder_path and os.path.exists(folder_path):
                    if include_sub:
                        # Delete everything inside recursively
                        for item in os.listdir(folder_path):
                            item_path = os.path.join(folder_path, item)
                            try:
                                if os.path.isfile(item_path) or os.path.islink(item_path):
                                    os.remove(item_path)
                                elif os.path.isdir(item_path):
                                    shutil.rmtree(item_path)
                            except Exception:
                                pass
                    else:
                        # Delete only files in main folder (ignore subfolders)
                        for item in os.listdir(folder_path):
                            item_path = os.path.join(folder_path, item)
                            if os.path.isfile(item_path):
                                try:
                                    os.remove(item_path)
                                except Exception:
                                    pass

        QMessageBox.information(self, "Done", "All files and subfolders in active folders have been deleted!")
