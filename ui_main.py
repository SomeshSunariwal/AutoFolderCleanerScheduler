# ui_main.py
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox
)
from PyQt6.QtCore import Qt
from ui_add_edit import AddEditDialog
from ui_settings import SettingsDialog
from storage import save_data
import os
import shutil
from PyQt6.QtWidgets import QMessageBox

class MainWindow(QMainWindow):
    def __init__(self, app_ref, data):
        super().__init__()
        self.app_ref = app_ref
        self.data = data
        self.setWindowTitle("AutoClean Scheduler")
        self.resize(900, 500)
        self.setup_ui()

    def setup_ui(self):
        central = QWidget()
        layout = QVBoxLayout()

        # ---------------- Top buttons ----------------
        top_layout = QHBoxLayout()
        top_layout.addStretch()  # push the button to the right

        # Big toggle button
        self.btn_schedule = QPushButton("Schedule")
        self.btn_schedule.setFixedSize(120, 50)  # big button
        self.btn_schedule.setStyleSheet("background-color: #0098FF; color: white; font-weight: bold; font-size: 15px; border-radius: 25px;")
        self.btn_schedule.setCheckable(True)  # allow toggle
        self.btn_schedule.clicked.connect(self.toggle_schedule)

        top_layout.addWidget(self.btn_schedule)
        layout.addLayout(top_layout)  # add above table

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(
            ["Folder Path", "Schedule", "Status", "Edit", "Delete"]
        )
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.table)

        # Buttons
        btn_layout = QHBoxLayout()
        self.btn_add = QPushButton("➕ Add Folder")
        self.btn_instant = QPushButton("⚡ Instant")   # NEW
        self.btn_settings = QPushButton("⚙️ Settings")
        self.btn_exit = QPushButton("❌ Exit")
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

    # -----------------------------
    # Populate the table
    # -----------------------------
    def populate_table(self):
        self.table.setRowCount(0)
        for i, folder in enumerate(self.data.get("folders", []), start=1):
            row = self.table.rowCount()
            self.table.insertRow(row)

            # Folder Path
            item = QTableWidgetItem(folder["path"])
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            item.setToolTip(folder["path"])  # <-- Add tooltip
            self.table.setItem(row, 0, item)
            self.table.setTextElideMode(Qt.TextElideMode.ElideMiddle)

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


    def toggle_schedule(self):
        """
        Temporary function to switch button state between Schedule and Stop.
        Later, we can connect it to actual scheduling service.
        """
        if self.btn_schedule.isChecked():
            # ON → Stop state
            self.btn_schedule.setText("Stop")
            self.btn_schedule.setStyleSheet("background-color: #F04444; color: white; font-weight: bold; font-size: 15px; border-radius: 25px;")
            print("Schedule stopped (temp)")
        else:
            # OFF → Schedule state
            self.btn_schedule.setText("Schedule")
            self.btn_schedule.setStyleSheet("background-color: #0098FF; color: white; font-weight: bold; font-size: 15px; border-radius: 25px;")
            print("Schedule started (temp)")