from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QStatusBar

class StatusBar:
    def __init__(self, parent):
        """Attach a QStatusBar to the given parent window"""
        self.parent = parent
        self.status_bar = QStatusBar()
        self.parent.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")

        # Style
        self.status_bar.setStyleSheet("""
            QStatusBar {
                background-color: #20232A;
                color: white;
                font-weight: 500;
                padding: 5px 10px;
                border-top: 1px solid #333;
            }
        """)

    def update_status(self, message, color="#22C55E", duration=5000):
        """Update the message and color"""
        self.status_bar.setStyleSheet(f"""
            QStatusBar {{
                background-color: #20232A;
                color: {color};
                font-weight: 500;
                padding: 5px 10px;
            }}
        """)
        self.status_bar.showMessage(message)
        QTimer.singleShot(duration, lambda: self.status_bar.showMessage("Ready"))
