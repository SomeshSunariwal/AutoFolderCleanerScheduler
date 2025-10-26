# task_scheduler.py
from PyQt6.QtCore import QObject, QTimer
import os, time

class TaskScheduler(QObject):
    def __init__(self, status_ui):
        super().__init__()
        self.status_ui = status_ui
        self.active_tasks = {}  # folder path -> QTimer
        self.is_running = False  # ensures only 1 task runs at a time

    def run(self, folder):
        """Start scheduler for a single folder"""
        path = folder['path']
        if path in self.active_tasks:
            self.status_ui.update_status(f"Scheduler already running for {path}", "#FACC15")
            return

        interval_ms = self._get_interval_ms(folder)
        timer = QTimer()
        timer.setInterval(interval_ms)
        timer.timeout.connect(lambda: self._run_task(folder))
        timer.start()

        self.active_tasks[path] = timer
        self.status_ui.update_status(f"Started scheduler for {path}", "#22C55E")
        print(f"[Run] Scheduler started for {path}")

    def runAll(self, folder=None):
        """Start scheduler for all active folders"""
        # folder parameter can be used to iterate over main window folders
        print("[RunAll] Starting all schedulers")
        self.status_ui.update_status("Started all schedules", "#22C55E")
        # TODO: Iterate all folders in your main_window and call self.run(folder)

    def remove(self, folder):
        """Stop scheduler for a single folder"""
        path = folder['path']
        if path in self.active_tasks:
            self.active_tasks[path].stop()
            del self.active_tasks[path]
            self.status_ui.update_status(f"Removed scheduler for {path}", "#EF4444")
            print(f"[Remove] Scheduler removed for {path}")

    def removeAll(self, folder=None):
        """Stop scheduler for all folders"""
        for path, timer in list(self.active_tasks.items()):
            timer.stop()
            del self.active_tasks[path]
        self.status_ui.update_status("Removed all schedules", "#EF4444")
        print("[RemoveAll] All schedulers removed")

    def pause(self, folder):
        """Pause scheduler for a single folder"""
        path = folder['path']
        if path in self.active_tasks:
            self.active_tasks[path].stop()
            self.status_ui.update_status(f"Paused scheduler for {path}", "#FACC15")
            print(f"[Pause] Scheduler paused for {path}")

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
        self.status_ui.update_status(f"Cleaning {path}...", "#FACC15")
        print(f"[Task] Cleaning {path}")

        self._clean_folder(folder)

        self.status_ui.update_status(f"Cleanup done for {path}", "#22C55E")
        print(f"[Task] Cleanup done for {path}")
        self.is_running = False

    def _clean_folder(self, folder):
        """Core cleanup logic"""
        base = folder['path']
        include_sub = folder.get('include_subfolders', True)
        older_than_hours = folder.get('older_than_value', 0)
        now = time.time()
        cutoff = now - (older_than_hours * 3600)

        for root, dirs, files in os.walk(base):
            for file in files:
                fpath = os.path.join(root, file)
                try:
                    if older_than_hours > 0:
                        if os.path.getmtime(fpath) < cutoff:
                            os.remove(fpath)
                    else:
                        os.remove(fpath)
                except Exception as e:
                    print(f"Error deleting {fpath}: {e}")

            if not include_sub:
                break
