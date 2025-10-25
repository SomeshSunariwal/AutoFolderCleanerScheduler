class TaskScheduler:

    def __init__(self, status_ui):
        """
        :param status_ui: Instance of StatusBar
        """
        self.status_ui = status_ui

    def toggle_run(self, folder, button_widget=None, checked=None):
        """
        Dummy function to test Play/Pause for a folder.
        :param folder: dict containing folder info
        :param button_widget: QPushButton object from the table cell
        :param checked: bool, state of the toggle button
        """
        if checked:
            # Button checked → Paused
            if button_widget:
                button_widget.setText("🟥")
                self.start_scheduler()
                button_widget.setStyleSheet("""
                QPushButton {
                    background-color: #F0F0F0;   /* Red for Pause */
                }
                QPushButton:hover {
                    background-color: #D63333;   /* Darker on hover */
                }
                    """)
            print(f"Scheduler running for folder: {folder['path']}")
        else:
            # Button unchecked → Running
            if button_widget:
                button_widget.setText("▶️")
                self.stop_scheduler()
                button_widget.setStyleSheet("")

            print(f"Scheduler paused for folder: {folder['path']}")


    # Future: add scheduled deletion functions here
    def start_scheduler(self):
        self.status_ui.update_status("Starting Scheduler...", "#FACC15")

        """Start the scheduler service (placeholder)"""

        self.status_ui.update_status("Running...", "#22C55E")   

        self.status_ui.update_status("Ready 1", "#22C55E") 



    def stop_scheduler(self):
        self.status_ui.update_status("Stopping Scheduler...", "#EF4444") 
        
        """Stop the scheduler service (placeholder)"""

        self.status_ui.update_status("Running...", "#22C55E")   
        
        self.status_ui.update_status("Ready 2", "#22C55E") 


    def toggle_schedule(self, button_widget, checked):
        """
        Temporary function to switch button state between Schedule All / Stop All.
        Later, connect it to the actual scheduling service.
        :param button_widget: QPushButton object
        :param checked: bool, button check state
        """
        if checked:
            # ON → Stop state
            button_widget.setText("Stop All")
            self.status_ui.update_status("Stopping All Scheduler...", "#FACC15") 
            button_widget.setStyleSheet(
                "background-color: #F04444; color: white; font-weight: bold; font-size: 15px; border-radius: 25px;"
            )
            print("Schedule stopped (temp)")
            self.status_ui.update_status("Running...", "#22C55E")   
        
            self.status_ui.update_status("Ready!", "#22C55E") 
        else:
            # OFF → Schedule state
            self.status_ui.update_status("Starting All Scheduler...", "#FACC15") 
            button_widget.setText("Schedule All")
            button_widget.setStyleSheet(
                "background-color: #0098FF; color: white; font-weight: bold; font-size: 15px; border-radius: 25px;"
            )
            print("Schedule started (temp)")
            self.status_ui.update_status("Running...", "#22C55E")   
            
            self.status_ui.update_status("Ready!", "#22C55E") 