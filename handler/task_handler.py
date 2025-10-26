from scheduler.task_scheduler import TaskScheduler
from utility.info_dialog_box import InfoDialogBox
from PyQt6.QtWidgets import QMessageBox

class TaskHandler:

    def __init__(self, main_window):
        self.main_window = main_window
        self.scheduler = TaskScheduler(main_window.status_ui)
        self.scheduler_running = False

    def toggle_run(self, folder, button_widget=None, checked=None):
        """
        Function to toggle individual folder run/pause.
        """
        is_active = folder.get("active", False)  # check if folder is active

        if checked and is_active:
            # 🟥 Paused / Running
            if button_widget:
                button_widget.setText("🟥")
                button_widget.setStyleSheet("""
                QPushButton {
                    background-color: #EDEDED;   /* Red for Pause */
                }
                QPushButton:hover {
                    background-color: #C2C2C2;   /* Darker on hover */
                }
                """)
                self.scheduler.run(folder)
        elif not is_active:
            InfoDialogBox._show_dialog("Info", 
                                       "Caution", 
                                       QMessageBox.Icon.Warning, 
                                       "Please Activate the Task First")
            button_widget.setChecked(False)
        else:
            # ▶️ Stopped
            if button_widget:
                button_widget.setText("▶️")
                button_widget.setStyleSheet("")
                self.scheduler.remove(folder)

    def toggle_schedule(self, all_button, checked):
        """
        Toggle the 'Schedule All' button.
        """
        self.scheduler_running = checked

        if checked:
            all_button.setText("Stop All")
            all_button.setStyleSheet("""
                    background-color: #F04444;
                    color: white;
                    font-weight: bold;
                    font-size: 15px;
                    border-radius: 25px;
            """)

            self.main_window.status_ui.update_status("Starting all schedule tasks...", "#FACC15", duration=3000)

            # Schedule all active folders
            for row in range(self.main_window.table.rowCount()):
                folder = self.main_window.data["folders"][row]
                run_btn = self.main_window.table.cellWidget(row, 5)
                if folder.get("active", True):
                    if run_btn:
                        run_btn.setChecked(True)  # Running
                        self.toggle_run(folder, run_btn, checked=True)

            self.main_window.status_ui.update_status("All schedules tasks running...", "#22C55E", duration=3000)

        else:
            all_button.setText("Schedule All")
            all_button.setStyleSheet("""
                    background-color: #0098FF;
                    color: white;
                    font-weight: bold;
                    font-size: 15px;
                    border-radius: 25px;
            """)
            self.main_window.status_ui.update_status("Stopping all scheduled tasks...", "#FACC15", duration=3000)

            for row in range(self.main_window.table.rowCount()):
                folder = self.main_window.data["folders"][row]
                run_btn = self.main_window.table.cellWidget(row, 5)
                if folder.get("active", True) and run_btn:
                    run_btn.setChecked(False)  # Paused
                    self.toggle_run(folder, run_btn, checked=False)

            self.main_window.status_ui.update_status("All scheduled tasks stopped", "#EF4444", duration=3000)

    
    def remove_task(self, folder):
        # if botton is pressed then remove the task:
        self.scheduler.remove(folder=folder)