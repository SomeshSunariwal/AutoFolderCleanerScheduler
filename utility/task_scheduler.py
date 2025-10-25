import time


class TaskScheduler:

    def __init__(self, main_window):
        self.main_window = main_window

    def toggle_run(self, folder, button_widget=None, checked=None):
        """
        Dummy function to toggle individual folder run/pause.
        """
        if checked:
            # Paused
            if button_widget:
                button_widget.setText("🟥")
                button_widget.setStyleSheet("background-color: #F5F5F5; font-size:16px; border-radius: 15px;")
                self.schedule_task(folder)
            print(f"Scheduler paused for folder: {folder['path']}")
        else:
            # Running
            if button_widget:
                button_widget.setText("▶️")
                button_widget.setStyleSheet("background-color: #FF7263; font-size:16px; border-radius: 15px;")
            print(f"Scheduler running for folder: {folder['path']}")


    def toggle_schedule(self, all_button, checked):
        """
        Toggle the 'Schedule All' button.
        """
        self.scheduler_running = checked

        if checked:
            all_button.setText("Stop All")
            all_button.setStyleSheet("""
                QPushButton {
                    background-color: #F04444;
                    color: white;
                    font-weight: bold;
                    font-size: 15px;
                    border-radius: 25px;
                }
            """)

            self.main_window.status_ui.update_status("Starting all schedules...", "#FACC15", duration=2000)

            # Schedule all active folders
            for row in range(self.main_window.table.rowCount()):
                folder = self.main_window.data["folders"][row]
                run_btn = self.main_window.table.cellWidget(row, 5)
                if folder.get("active", True):
                    if run_btn:
                        run_btn.setChecked(False)  # Running
                        self.toggle_run(folder, run_btn, checked=True)

            self.main_window.status_ui.update_status("All schedules running...", "#22C55E")

        else:
            all_button.setText("Schedule All")
            all_button.setStyleSheet("""
                QPushButton {
                    background-color: #0098FF;
                    color: white;
                    font-weight: bold;
                    font-size: 15px;
                    border-radius: 25px;
                }
            """)
            self.main_window.status_ui.update_status("Stopping all schedules...", "#FACC15", duration=2000)

            for row in range(self.main_window.table.rowCount()):
                folder = self.main_window.data["folders"][row]
                run_btn = self.main_window.table.cellWidget(row, 5)
                if folder.get("active", True) and run_btn:
                    run_btn.setChecked(True)  # Paused
                    self.toggle_run(folder, run_btn, checked=False)

            self.main_window.status_ui.update_status("All schedules stopped", "#EF4444")

    def schedule_task(self, folder):
        """
        Dummy placeholder function to schedule a folder.
        Replace this with actual scheduling logic later.
        """
        print(f"[Scheduled Task Placeholder] Folder: {folder['path']}")
        # Example: simulate processing time
        # time.sleep(0.5)  # optional for testing