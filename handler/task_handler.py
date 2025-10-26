from scheduler.task_scheduler import TaskScheduler

class TaskHandler:

    def __init__(self, main_window):
        self.main_window = main_window
        self.scheduler = TaskScheduler(main_window.status_ui)
        self.scheduler_running = False

    def toggle_run(self, folder, button_widget=None, checked=None):
        """
        Dummy function to toggle individual folder run/pause.
        """
        if checked:
            # Paused
            if button_widget:
                button_widget.setText("🟥")
                # run the task
                self.scheduler.run(folder)
                # button_widget.setFocusPolicy(Qt.FocusPolicy.NoFocus)
                print(f"Scheduler running for folder: {folder['path']}")
        else:
            # Running
            if button_widget:
                button_widget.setText("▶️")
                self.scheduler.remove(folder)
                # button_widget.setFocusPolicy(Qt.FocusPolicy.NoFocus)
                print(f"Scheduler paused for folder: {folder['path']}")

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

    # def schedule_task(self, folder, action="run", checked=None):
    #         """
    #         Single entry point for all TaskScheduler operations.
    #         folder : dict containing folder data
    #         action : str, one of ['run', 'runAll', 'remove', 'removeAll', 'pause', 'toggle']
    #         checked: bool, used for toggle action
    #         """

    #         print(folder)

    #         if action == "run":
    #             self.scheduler.run(folder)
    #         elif action == "runAll":
    #             self.scheduler.runAll(folder)
    #         elif action == "remove":
    #             self.scheduler.remove(folder)
    #         elif action == "removeAll":
    #             self.scheduler.removeAll(folder)
    #         elif action == "pause":
    #             self.scheduler.pause(folder)
    #         elif action == "toggle":
    #             if checked:
    #                 self.scheduler.run(folder)
    #             else:
    #                 self.scheduler.pause(folder)