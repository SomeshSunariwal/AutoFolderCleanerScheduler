from utility.window_register import WindowServiceRegister

class RegisterHandler:
    def __init__(self, main_window):
        self.window_register = WindowServiceRegister(main_window.status_ui)
        
    def toggle_startup(self, button, checked):
        if checked:
            self.window_register.register_startup()
            button.setText("Remove from Startup")
            button.setStyleSheet("""
                background-color: #F87171;
                font-weight: bold;
                font-size: 14px;
                border-radius: 25px;
            """)
        else:
            self.window_register.deregister_startup()
            button.setText("Run in Background")
            button.setStyleSheet("""
                background-color: #22C55E;
                font-weight: bold;
                font-size: 14px;
                border-radius: 25px;
            """)

