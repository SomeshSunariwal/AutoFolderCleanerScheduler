# task_scheduler.py
def toggle_run(folder, button_widget=None, checked=None):
    """
    Dummy function to test Play/Pause for a folder.
    :param folder: dict containing folder info
    :param button_widget: QPushButton object from the table cell
    :param checked: bool, state of the toggle button
    """
    if checked:
        # Button checked → Paused
        if button_widget:
            button_widget.setText("⏸️")
            button_widget.setStyleSheet("""
             QPushButton {
                background-color: #F04444;   /* Red for Pause */
            }
            QPushButton:hover {
                background-color: #D63333;   /* Darker on hover */
            }
                """)
        print(f"Scheduler paused for folder: {folder['path']}")
    else:
        # Button unchecked → Running
        if button_widget:
            button_widget.setText("▶️")
            button_widget.setStyleSheet("")

        print(f"Scheduler running for folder: {folder['path']}")


# Future: add scheduled deletion functions here
def start_scheduler():
    """Start the scheduler service (placeholder)"""
    print("Scheduler service started (placeholder).")


def stop_scheduler():
    """Stop the scheduler service (placeholder)"""
    print("Scheduler service stopped (placeholder).")


def toggle_schedule(button_widget, checked):
    """
    Temporary function to switch button state between Schedule All / Stop All.
    Later, connect it to the actual scheduling service.
    :param button_widget: QPushButton object
    :param checked: bool, button check state
    """
    if checked:
        # ON → Stop state
        button_widget.setText("Stop All")
        button_widget.setStyleSheet(
            "background-color: #F04444; color: white; font-weight: bold; font-size: 15px; border-radius: 25px;"
        )
        print("Schedule stopped (temp)")
    else:
        # OFF → Schedule state
        button_widget.setText("Schedule All")
        button_widget.setStyleSheet(
            "background-color: #0098FF; color: white; font-weight: bold; font-size: 15px; border-radius: 25px;"
        )
        print("Schedule started (temp)")