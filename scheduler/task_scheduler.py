# task_scheduler.py
from PyQt6.QtCore import QObject, QTimer
import os, time, shutil
from PyQt6.QtWidgets import QMessageBox

class TaskScheduler(QObject):
    def __init__(self, status_ui, info_box):
        super().__init__()
        self.status_ui = status_ui
        self.info_box = info_box
        self.active_tasks = {}  # folder path -> QTimer
        self.is_running = False  # ensures only 1 task runs at a time

    def run(self, folder):
        """Start scheduler for a single folder"""
        path = folder['path']
        if path in self.active_tasks:
            self.status_ui.update_status(f"[Start] Scheduler already running for {path}", "#FACC15", duration=3000)
            return

        interval_ms = self._get_interval_ms(folder)
        timer = QTimer()
        timer.setInterval(interval_ms)
        timer.timeout.connect(lambda: self._run_task(folder))
        timer.start()
        self.active_tasks[path] = timer
        self.status_ui.update_status(f"[Started] scheduler for {path}", "#22C55E", duration=3000)

    def runAll(self, folder=None):
        """Start scheduler for all active folders"""
        # folder parameter can be used to iterate over main window folders
        self.status_ui.update_status("[Started] all schedules", "#22C55E")
        # TODO: Iterate all folders in your main_window and call self.run(folder)

    def remove(self, folder):
        """Stop scheduler for a single folder"""
        path = folder['path']
        if path in self.active_tasks:
            self.active_tasks[path].stop()
            del self.active_tasks[path]
            self.status_ui.update_status(f"[Removed] scheduler for {path}", "#EF4444", duration=3000)

    def removeAll(self, folder=None):
        """Stop scheduler for all folders"""
        for path, timer in list(self.active_tasks.items()):
            timer.stop()
            del self.active_tasks[path]
        self.status_ui.update_status("[Removed] all schedules", "#EF4444", duration=3000)
        # TODO: Future Work

    def pause(self, folder):
        """Pause scheduler for a single folder"""
        path = folder['path']
        if path in self.active_tasks:
            self.active_tasks[path].stop()
            self.status_ui.update_status(f"[Paused] scheduler for {path}", "#FACC15", duration=3000)

    def resume(self, folder):
        """Resume scheduler for a single folder"""
        path = folder['path']
        if path in self.active_tasks:
            self.active_tasks[path].start()
            self.status_ui.update_status(f"[Resume] scheduler for {path}", "#FACC15", duration=3000)

    # ----- Internal helper functions -----
    def _get_interval_ms(self, folder):
        value = folder.get('interval_value', 5)
        unit = folder.get('interval_unit', 'seconds')

        # Multiplier: convert unit to milliseconds
        multiplier = {
            'seconds': 1000,
            'minutes': 60 * 1000,
            'hours': 3600 * 1000,
            'days': 24 * 3600 * 1000
        }.get(unit, 1000)  # default to 1 second if unknown

        return value * multiplier

    def _run_task(self, folder):
        """Actual folder cleanup"""
        if self.is_running:
            # skip if another task is running
            return

        self.is_running = True
        path = folder['path']
        self.status_ui.update_status(f"Cleaning {path}...", "#FACC15", duration=3000)

        self._clean_folder(folder)

        self.status_ui.update_status(f"Cleanup done for {path}", "#22C55E", duration=3000)
        self.is_running = False

    def _clean_folder(self, folder):
        """Core cleanup logic deleting all files and folders, including non-empty subfolders"""
        base = folder['path']
        include_sub = folder.get('include_subfolders', True)
        older_than_value = folder.get('older_than_value', 0)
        older_than_unit = folder.get('older_than_unit', 'hours').lower()
        now = time.time()

        # Convert older_than_value to seconds
        unit_multipliers = {
            'seconds': 1,
            'minutes': 60,
            'hours': 3600,
            'days': 24 * 3600
        }
        multiplier = unit_multipliers.get(older_than_unit, 3600)  # default hours
        cutoff = now - (older_than_value * multiplier)

        if include_sub:
            # Walk all folders and subfolders from bottom up
            for root, dirs, files in os.walk(base, topdown=False):
                # Delete files first
                for file in files:
                    fpath = os.path.join(root, file)
                    try:
                        if older_than_value > 0:
                            if os.path.getmtime(fpath) < cutoff:
                                os.remove(fpath)
                        else:
                            os.remove(fpath)
                    except Exception as e:
                        pass

                # Delete all subfolders regardless of empty/non-empty
                for dir in dirs:
                    dir_path = os.path.join(root, dir)
                    try:
                        shutil.rmtree(dir_path)
                    except Exception as e:
                        pass

        else:
            # Only delete files in the main folder (no recursion)
            try:
                for file in os.listdir(base):
                    fpath = os.path.join(base, file)
                    if os.path.isfile(fpath):
                        if older_than_value > 0:
                            if os.path.getmtime(fpath) < cutoff:
                                os.remove(fpath)
                        else:
                            os.remove(fpath)
            except Exception as e:
                pass