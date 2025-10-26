# ui_main.py
from PyQt6.QtWidgets import (
    QMainWindow, 
    QWidget, 
    QVBoxLayout, 
    QHBoxLayout, 
    QPushButton,
    QTableWidget, 
    QTableWidgetItem, 
    QHeaderView, 
    QMessageBox,
    QApplication, 
    QSystemTrayIcon, 
    QMenu
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QAction
from ui.ui_add_edit import AddEditDialog
from ui.ui_settings import SettingsDialog
from utility.storage import save_data
from handler.task_handler import TaskHandler
from utility.status import StatusBar
from utility.instant_delete import instant_delete
from utility.info_dialog_box import InfoDialogBox
from handler.register_handler import RegisterHandler
import sys, os


class MainWindow(QMainWindow):
    def __init__(self, app_ref, data):
        super().__init__()
        self.app_ref = app_ref
        self.data = data
        
        self.setWindowTitle("AutoClean Scheduler")
        self.setWindowIcon(QIcon(self.resource_path(os.path.join("ico", "main.ico"))))
        self.setFixedSize(1200, 700)

         # --- System Tray Setup ---
        self.tray_icon = QSystemTrayIcon(QIcon(self.resource_path(os.path.join("ico", "main.ico"))), self)
              
        # Create context menu
        tray_menu = QMenu()
        show_action = QAction("Show Window")
        quit_action = QAction("Exit App")
        tray_menu.addAction(show_action)
        tray_menu.addAction(quit_action)

        # Attach menu to tray icon
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.setToolTip("AutoClean Scheduler")

        # Connect actions
        show_action.triggered.connect(self.show_window)
        quit_action.triggered.connect(self.exit_app)

        # Left-click restores window
        self.tray_icon.activated.connect(self.on_tray_icon_activated)


        # ✅ Create StatusBar instance here
        self.status_ui = StatusBar(self)
        
       # ✅ Create InfoDialogBox instance here
        self.info_box = InfoDialogBox()

        # ✅ Create TaskScheduler instance here
        self.task = TaskHandler(self)

        # ✅ Create RegisterHandler instance here
        self.register_handler = RegisterHandler(self)

        # Initialize UI
        self.setup_ui()
 
        # Restart from old state after restart
        self.restore_active_schedules()

    # Override closeEvent to minimize to tray
    def closeEvent(self, event):
        """Window 'X' button quits completely"""
        self.tray_icon.hide()  # remove tray icon
        QApplication.quit()
    
    def hide_to_tray(self):
        """Hide window to tray when Exit button is clicked"""
        self.tray_icon.show()
        self.hide()
        self.tray_icon.showMessage(
            "Windows Auto Folder Cleaner",
            "Application is still running in the system tray",
            QSystemTrayIcon.MessageIcon.Information,
            3000
        )

    def on_tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:  # left click
            self.show_window()
            self.tray_icon.hide()

    # Show window from tray
    def show_window(self):
        self.show()
        self.raise_()          # Bring window to top
        self.activateWindow()  # Give focus to the window

    # Quit app properly
    def exit_app(self):
        self.tray_icon.hide()  # hide tray icon first
        QApplication.quit()

    def resource_path(self, relative_path):
        """Get absolute path to resource (works for dev & for PyInstaller .exe)"""
        try:
            # When running as .exe
            base_path = sys._MEIPASS
        except Exception:
            # When running as script
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)
    
    def restore_active_schedules(self):
        for row, folder in enumerate(self.data.get("folders", [])):
            if folder.get("running", False):
                try:
                    self.task.run_task(folder=folder)
                    btn = self.table.cellWidget(row, 5)
                    if btn:
                        btn.setChecked(True)
                        btn.setText("🟥")  # indicate it's running
                    self.status_ui.update_status("All Task Restored...", "#22C55E", duration=3000)
                except Exception as e:
                    self.info_box._show_dialog("Error Box", 
                                               "Error Occur",
                                               QMessageBox.Icon.Critical, 
                                               f"[AutoStart] Failed to restore {folder['path']}: {e}")

    def setup_ui(self):
        button_height = 40  # desired height in pixels
        central = QWidget()
        layout = QVBoxLayout()

        # ---------------- Top buttons ----------------
        top_layout = QHBoxLayout()
        top_layout.addStretch()  # push the button to the right

        # --- Run in Background Button ---
        self.btn_run_bg = QPushButton("Run in Background")
        self.btn_run_bg.setFixedSize(150, 50)
        self.btn_run_bg.setStyleSheet("""
           background-color: #22C55E;
            font-weight: bold;
            font-size: 14px;
            border-radius: 25px;
        """)
        self.btn_run_bg.setCheckable(True)  # allow toggle
        self.btn_run_bg.clicked.connect(
            lambda checked: self.register_handler.toggle_startup(self.btn_run_bg, checked)
        )

        top_layout.addWidget(self.btn_run_bg)

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
            ["Folder Path", "Schedule", "Task Status", "Edit", "Delete", "Run"]
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
        self.btn_exit = QPushButton("👁️ Hide in Tray")
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
        self.btn_instant.clicked.connect(lambda: instant_delete(self=self))
        self.btn_settings.clicked.connect(self.open_settings)
        self.btn_exit.clicked.connect(self.hide_to_tray)

        self.populate_table()
        self.status_ui.update_status("Ready!", "#22C55E", duration=3000)

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
            status_item = QTableWidgetItem("Enable" if folder["active"] else "Disabled")
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
            folder_data["running"] = False
            print(folder_data)
            # Check for duplicate folder path
            existing_paths = [f['path'].lower() for f in self.data.get("folders", [])]
            if folder_data['path'].lower() in existing_paths:
                # Show error dialog if duplicate
                self.info_box._show_dialog("Info Box", 
                                           "Information: ",
                                           QMessageBox.Icon.Information,
                                           f"Folder \"{folder_data['path']}\" is already present.")
                return  # Stop adding

            # No duplicate → add folder
            self.data.setdefault("folders", []).append(folder_data)
            save_data(self.data)
            self.populate_table()  # Refresh dashboard

    # -----------------------------
    # Edit Folder
    # -----------------------------
    def edit_folder(self, row):
        folder = self.data["folders"][row]
        # Then Change the switch as well
        self.task.toggle_run(self.data["folders"][row], self.table.cellWidget(row, 5), False, True)
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
            # First delete the task then remove
            self.task.remove_task(self.data["folders"][row])
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
