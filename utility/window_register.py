import os
import sys
import pythoncom 
from win32com.shell import shell

class WindowServiceRegister:
    def __init__(self, status_ui):
        self.status = status_ui
        
    def register_startup(self):
        """Add app shortcut to Windows startup folder"""
        startup_folder = os.path.join(os.getenv('APPDATA'), r'Microsoft\Windows\Start Menu\Programs\Startup')
        exe_path = sys.executable  # path to your python exe / packaged exe

        # Name of the shortcut
        shortcut_path = os.path.join(startup_folder, "Windows Auto Folder Cleaner.lnk")

        try:
            # Only create if it doesn't exist
            if not os.path.exists(shortcut_path):
            
                # Create a shortcut
                shell_link = pythoncom.CoCreateInstance(
                    shell.CLSID_ShellLink, None,
                    pythoncom.CLSCTX_INPROC_SERVER, shell.IID_IShellLink
                )
                shell_link.SetPath(exe_path)
                shell_link.SetWorkingDirectory(os.path.dirname(exe_path))
                shell_link.SetDescription("Windows Auto Folder Cleaner")
                
                persist_file = shell_link.QueryInterface(pythoncom.IID_IPersistFile)
                persist_file.Save(shortcut_path, 0)

            self.status.update_status("Registered for startup successfully!", "#22C55E", 5000)
        except Exception as e:
            self.status.update_status(f"Failed to register startup: {e}", "#EF4444", 5000)

    def deregister_startup(self):
        """Remove app from Windows startup"""
        startup_folder = os.path.join(os.getenv('APPDATA'), r'Microsoft\Windows\Start Menu\Programs\Startup')
        shortcut_path = os.path.join(startup_folder, "Windows Auto Folder Cleaner.lnk")

        try:
            if os.path.exists(shortcut_path):
                os.remove(shortcut_path)
                self.status.update_status("Removed from startup successfully!", "#F87171", 5000)
            else:
                self.status.update_status("App is not registered in startup.", "#FACC15", 5000)
        except Exception as e:
            self.status.update_status(f"Failed to remove startup: {e}", "#EF4444", 5000)
