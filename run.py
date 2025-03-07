import os
import sys
import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class ChangeHandler(FileSystemEventHandler):
    def __init__(self, script):
        self.script = script
        self.process = None
        self.start_bot()

    def start_bot(self):
        if self.process:
            self.process.kill()
        self.process = subprocess.Popen([sys.executable, self.script])

    def on_modified(self, event):
        if event.src_path.endswith(".py"):
            print(f"{event.src_path} has been modified. Restarting bot...")
            self.start_bot()

    def on_created(self, event):
        if event.src_path.endswith(".py"):
            print(f"{event.src_path} has been created. Restarting bot...")
            self.start_bot()

if __name__ == "__main__":
    script = "main.py"  # bot's main script
    event_handler = ChangeHandler(script)
    observer = Observer()
    observer.schedule(event_handler, path=".", recursive=True)
    observer.start()
    
    print(f"Watching for changes in {script}...")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
