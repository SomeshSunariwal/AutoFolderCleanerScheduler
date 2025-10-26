from scheduler.task_scheduler import TaskScheduler
from utility.info_dialog_box import ErrorHandle

class TaskHandler:

    def __init__(self, main_window):
        self.main_window = main_window
        self.scheduler = TaskScheduler(main_window.status_ui)
        self.scheduler_running = False

    def toggle_run(self, folder, button_widget=None, checked=None):
        """
        function to toggle individual folder run/pause.
        """
        if checked:
            # Paused
            if button_widget:
                button_widget.setText("🟥")
                # run the task
                self.scheduler.run(folder)             
        else:
            # Running
            if button_widget:
                button_widget.setText("▶️")
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

            self.main_window.status_ui.update_status("Starting all schedules...", "#FACC15", duration=2000)

            # Schedule all active folders
            for row in range(self.main_window.table.rowCount()):
                folder = self.main_window.data["folders"][row]
                run_btn = self.main_window.table.cellWidget(row, 5)
                if folder.get("active", True):
                    if run_btn:
                        run_btn.setChecked(True)  # Running
                        self.toggle_run(folder, run_btn, checked=True)

            self.main_window.status_ui.update_status("All schedules running...", "#22C55E")

        else:
            all_button.setText("Schedule All")
            all_button.setStyleSheet("""
                    background-color: #0098FF;
                    color: white;
                    font-weight: bold;
                    font-size: 15px;
                    border-radius: 25px;
            """)
            self.main_window.status_ui.update_status("Stopping all schedules...", "#FACC15", duration=2000)

            for row in range(self.main_window.table.rowCount()):
                folder = self.main_window.data["folders"][row]
                run_btn = self.main_window.table.cellWidget(row, 5)
                if folder.get("active", True) and run_btn:
                    run_btn.setChecked(False)  # Paused
                    self.toggle_run(folder, run_btn, checked=False)

            self.main_window.status_ui.update_status("All schedules stopped", "#EF4444")

    
    def remove_task(self, folder):
        # if botton is pressed then remove the task:
        self.scheduler.remove(folder=folder)