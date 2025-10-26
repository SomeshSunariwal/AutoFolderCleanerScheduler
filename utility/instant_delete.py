import os
from PyQt6.QtWidgets import QMessageBox

def instant_delete(self):
    """
    Delete all files in folders that are Active immediately.
    """
    reply = QMessageBox.question(
        self, "Instant Delete",
        "Are you sure you want to delete ALL files in all Active folders?",
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
    )
    if reply != QMessageBox.StandardButton.Yes:
        return

    for folder in self.data.get("folders", []):
        if folder.get("active", True):  # Only active folders
            folder_path = folder.get("path")
            include_sub = folder.get("include_subfolders", True)
            if folder_path and os.path.exists(folder_path):
                if include_sub:
                    # Delete all files recursively
                    for root, dirs, files in os.walk(folder_path):
                        for file in files:
                            try:
                                os.remove(os.path.join(root, file))
                            except Exception:
                                pass
                else:
                    # Delete only files in the main folder
                    for file in os.listdir(folder_path):
                        fpath = os.path.join(folder_path, file)
                        if os.path.isfile(fpath):
                            try:
                                os.remove(fpath)
                            except Exception:
                                pass

    QMessageBox.information(self, "Done", "All files in active folders have been deleted!")
