#!/usr/bin/env python3
"""
Development watcher script for the clinic app.
Automatically restarts the application when Python files are modified.
"""

import os
import sys
import time
import subprocess
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class AppRestartHandler(FileSystemEventHandler):
    def __init__(self, script_path):
        self.script_path = script_path
        self.process = None
        self.restart_app()

    def on_modified(self, event):
        if event.is_directory:
            return
        
        # Only restart on Python file changes
        if event.src_path.endswith('.py'):
            print(f"\n📁 File changed: {event.src_path}")
            print("🔄 Restarting application...")
            self.restart_app()

    def restart_app(self):
        # Kill existing process
        if self.process:
            try:
                self.process.terminate()
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()
                self.process.wait()
            except Exception as e:
                print(f"Error stopping process: {e}")

        # Start new process
        try:
            print(f"🚀 Starting {self.script_path}...")
            self.process = subprocess.Popen([sys.executable, self.script_path])
            print("✅ Application started successfully!")
        except Exception as e:
            print(f"❌ Error starting application: {e}")

def main():
    # Path to your main script
    script_path = Path(__file__).parent / "main.py"
    
    if not script_path.exists():
        print(f"❌ Error: {script_path} not found!")
        sys.exit(1)

    print("🔍 Clinic App Development Watcher")
    print("=" * 40)
    print(f"📂 Watching directory: {Path.cwd()}")
    print(f"🎯 Target script: {script_path}")
    print("📝 Watching for changes in .py files")
    print("🔄 Auto-restart enabled")
    print("⚠️  Press Ctrl+C to stop")
    print("=" * 40)

    # Set up file watcher
    event_handler = AppRestartHandler(str(script_path))
    observer = Observer()
    observer.schedule(event_handler, path=str(Path.cwd()), recursive=True)
    
    try:
        observer.start()
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping watcher...")
        observer.stop()
        if event_handler.process:
            try:
                event_handler.process.terminate()
                event_handler.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                event_handler.process.kill()
                event_handler.process.wait()
        print("👋 Goodbye!")
    
    observer.join()

if __name__ == "__main__":
    main()
