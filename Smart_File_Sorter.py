#!/usr/bin/env python3
"""
Smart File Sorter - Automated File Organization Tool
Author: Anurag Wanwe
Description: Monitors folders and automatically organizes files by type with smart features
"""

from fileinput import filename
import os
import sys
import shutil
import json
import hashlib
import pystray
import psutil
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import socket
import tempfile

def get_app_dir():
    """Returns base directory for app data (AppData)"""
    base = Path(os.getenv("APPDATA")) / "SmartFileSorter"
    base.mkdir(parents=True, exist_ok=True)
    return base

APP_DIR = get_app_dir()
CONFIG_FILE = APP_DIR / "config.json"
HISTORY_FILE = APP_DIR / "history.json"
STATS_FILE = APP_DIR / "stats.json"
LOCK_FILE = APP_DIR / "app.lock"


def is_already_running():
    """Check if another instance is already running"""
    try:
        # Create lock file with process ID
        if LOCK_FILE.exists():
            try:
                with open(LOCK_FILE, 'r') as f:
                    pid = int(f.read().strip())
                    
                # Check if process is actually running
                if sys.platform == 'win32':
                    
                    if psutil.pid_exists(pid):
                        return True
                    else:
                        # Stale lock file, remove it
                        LOCK_FILE.unlink()
            except:
                # If we can't read the lock file, assume it's stale
                LOCK_FILE.unlink()
        
        # Create new lock file
        with open(LOCK_FILE, 'w') as f:
            f.write(str(os.getpid()))
        return False
    except:
        return False


def cleanup_lock():
    """Remove lock file on exit"""
    try:
        if LOCK_FILE.exists():
            LOCK_FILE.unlink()
    except:
        pass


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)


class Config:
    """Configuration manager for the file sorter"""
    
    DEFAULT_CATEGORIES = {
        'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp', '.ico', '.tiff'],
        'Documents': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt', '.xls', '.xlsx', '.ppt', '.pptx'],
        'Videos': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.m4v'],
        'Audio': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma', '.m4a'],
        'Archives': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz'],
        'Code': ['.py', '.js', '.html', '.css', '.java', '.cpp', '.c', '.h', '.json', '.xml', '.sql'],
        'Executables': ['.exe', '.msi', '.app', '.dmg', '.deb', '.rpm'],
        'Others': []  # Catch-all category
    }
    
    def __init__(self):
        self.config_file = CONFIG_FILE
        self.categories = self.DEFAULT_CATEGORIES.copy()
        self.watched_folder = None
        self.enable_duplicates = True
        self.enable_undo = True
        self.load_config()
    
    def load_config(self):
        """Load configuration from file"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    data = json.load(f)
                    self.categories = data.get('categories', self.DEFAULT_CATEGORIES)
                    self.watched_folder = data.get('watched_folder')
                    self.enable_duplicates = data.get('enable_duplicates', True)
                    self.enable_undo = data.get('enable_undo', True)
            except Exception as e:
                print(f"Error loading config: {e}")
    
    def save_config(self):
        """Save configuration to file"""
        data = {
            'categories': self.categories,
            'watched_folder': self.watched_folder,
            'enable_duplicates': self.enable_duplicates,
            'enable_undo': self.enable_undo
        }
        with open(self.config_file, 'w') as f:
            json.dump(data, f, indent=4)


class FileOrganizer:
    """Core file organization logic"""
    
    def __init__(self, config):
        self.config = config
        self.history = []
        self.history_file = HISTORY_FILE
        self.stats = defaultdict(int)
        self.duplicates = {}
        self.load_history()
    
    def load_history(self):
        """Load move history for undo functionality"""
        if self.history_file.exists():
            try:
                with open(self.history_file, 'r') as f:
                    self.history = json.load(f)
            except Exception as e:
                print(f"Error loading history: {e}")
    
    def save_history(self):
        """Save move history"""
        with open(self.history_file, 'w') as f:
            json.dump(self.history[-100:], f, indent=4)  # Keep last 100 operations
    
    def get_file_hash(self, filepath):
        """Calculate MD5 hash of file for duplicate detection"""
        hash_md5 = hashlib.md5()
        try:
            with open(filepath, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except Exception:
            return None
    
    def get_category(self, filename):
        """Determine the category of a file based on its extension"""
        ext = Path(filename).suffix.lower()
        
        for category, extensions in self.config.categories.items():
            if ext in extensions:
                return category
        
        return 'Others'
    
    def organize_file(self, file_path, base_folder):
        """Organize a single file"""
        if not os.path.exists(file_path) or os.path.isdir(file_path):
            return None
        
        # Ignore hidden files and the config files
        if os.path.basename(file_path).startswith('.') or \
           os.path.basename(file_path) in ['config.json', 'history.json', 'stats.json']:
            return None
        
        try:
            category = self.get_category(file_path)
            category_folder = os.path.join(base_folder, category)
            
            # Create category folder if it doesn't exist
            os.makedirs(category_folder, exist_ok=True)
            
            filename = os.path.basename(file_path)
            destination = os.path.join(category_folder, filename)
            
            # Check for duplicates
            if self.config.enable_duplicates:
                file_hash = self.get_file_hash(file_path)
                if file_hash:
                    if file_hash in self.duplicates:
                        # File is a duplicate
                        dup_folder = os.path.join(base_folder, 'Duplicates')
                        os.makedirs(dup_folder, exist_ok=True)
                        destination = os.path.join(dup_folder, filename)
                        category = 'Duplicates'
                    else:
                        self.duplicates[file_hash] = file_path
            
            # Handle filename conflicts
            counter = 1
            base_name, extension = os.path.splitext(filename)
            while os.path.exists(destination):
                new_filename = f"{base_name}_{counter}{extension}"
                destination = os.path.join(os.path.dirname(destination), new_filename)
                counter += 1
            
            # Move the file
            shutil.move(file_path, destination)
            
            # Record the move
            if self.config.enable_undo:
                self.history.append({
                    'source': file_path,
                    'destination': destination,
                    'timestamp': datetime.now().isoformat(),
                    'category': category
                })
                self.save_history()
            
            # Update stats
            self.stats[category] += 1
            
            return destination
        
        except Exception as e:
            print(f"Error organizing {file_path}: {e}")
            return None
    
    def undo_last_move(self):
        """Undo the last file move operation"""
        if not self.history:
            return False, "No operations to undo"
        
        last_op = self.history.pop()
        try:
            if os.path.exists(last_op['destination']):
                # Recreate source directory if needed
                os.makedirs(os.path.dirname(last_op['source']), exist_ok=True)
                shutil.move(last_op['destination'], last_op['source'])
                self.save_history()
                return True, f"Undone: {os.path.basename(last_op['source'])}"
            else:
                return False, "File no longer exists"
        except Exception as e:
            self.history.append(last_op)  # Re-add if failed
            return False, f"Error: {e}"
    
    def get_stats(self):
        """Get organization statistics"""
        return dict(self.stats)


class FileWatcher(FileSystemEventHandler):
    """Watches for file system changes"""
    
    def __init__(self, organizer, base_folder, callback=None):
        self.organizer = organizer
        self.base_folder = base_folder
        self.callback = callback
        self.processing = set()
    
    def on_created(self, event):
        """Handle file creation events"""
        if event.is_directory:
            return
        
        file_path = event.src_path
        
        # Avoid processing files in category folders
        rel_path = os.path.relpath(file_path, self.base_folder)
        if os.path.dirname(rel_path) != '':
            return
        
        # Avoid processing the same file multiple times
        if file_path in self.processing:
            return
        
        self.processing.add(file_path)
        
        # Small delay to ensure file is completely written
        time.sleep(0.5)
        
        if os.path.exists(file_path):
            result = self.organizer.organize_file(file_path, self.base_folder)
            if result and self.callback:
                self.callback(f"Organized: {os.path.basename(result)}")
        
        self.processing.discard(file_path)


class SmartFileSorterGUI:
    """Main GUI application"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Smart File Sorter")
        self.root.geometry("800x600")
        
        self.config = Config()
        self.organizer = FileOrganizer(self.config)
        self.observer = None
        self.watching = False
        self.tray_icon = None
        self.tray_thread = None
        self.is_closing = False
        
        self.setup_ui()
        
        if self.config.watched_folder:
            self.folder_var.set(self.config.watched_folder)
        
        # Set up window close handler
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Set up window minimize handler
        self.root.bind("<Unmap>", self.on_minimize)
        self.minimized_by_user = False

    def on_minimize(self, event):
        """Handle window minimize event"""
        # Check if window is being iconified (minimized)
        if self.root.state() == 'iconic' and not self.is_closing:
            self.root.after(100, self.hide_to_tray)
    
    def hide_to_tray(self):
        """Hide window to system tray"""
        self.root.withdraw()
        self.log("Application minimized to tray")

    def setup_tray(self):
        """Setup system tray icon"""
        import pystray
        from PIL import Image
        
        # Load tray icon from bundled resource
        try:
            icon_path = resource_path("tray_icon.ico")
            icon_image = Image.open(icon_path)
        except Exception as e:
            print(f"Error loading tray icon: {e}")
            # Fallback to creating a simple icon
            icon_image = Image.new("RGB", (64, 64), "#4CAF50")
        
        self.tray_icon = pystray.Icon(
            "SmartFileSorter",
            icon_image,
            "Smart File Sorter",
            menu=pystray.Menu(
                pystray.MenuItem("Show Window", self.tray_show),
                pystray.MenuItem("Start Monitoring", self.tray_start, enabled=lambda item: not self.watching),
                pystray.MenuItem("Stop Monitoring", self.tray_stop, enabled=lambda item: self.watching),
                pystray.MenuItem("Exit", self.tray_exit)
            )
        )
        
        self.tray_icon.run()

    def tray_start(self, icon=None, item=None):
        """Start monitoring from tray"""
        if not self.watching:
            self.root.after(0, self.start_monitoring)

    def tray_stop(self, icon=None, item=None):
        """Stop monitoring from tray"""
        if self.watching:
            self.root.after(0, self.stop_monitoring)

    def tray_show(self, icon=None, item=None):
        """Show window from tray"""
        self.root.after(0, self.root.deiconify)
        self.root.after(0, self.root.lift)
        self.root.after(0, self.root.focus_force)

    def tray_exit(self, icon=None, item=None):
        """Exit application from tray"""
        self.is_closing = True
        if self.observer:
            self.observer.stop()
        if icon:
            icon.stop()
        self.root.after(0, self.root.quit)

    def setup_ui(self):
        """Setup the user interface"""
        # Set application icon
        try:
            icon_path = resource_path("app_icon.ico")
            self.root.iconbitmap(icon_path)
        except Exception as e:
            print(f"Error setting app icon: {e}")
        
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(3, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Smart File Sorter", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, pady=10)
        
        # Folder selection
        folder_frame = ttk.LabelFrame(main_frame, text="Folder to Monitor", padding="10")
        folder_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)
        folder_frame.columnconfigure(0, weight=1)
        
        self.folder_var = tk.StringVar()
        folder_entry = ttk.Entry(folder_frame, textvariable=self.folder_var, width=50)
        folder_entry.grid(row=0, column=0, padx=(0, 5), sticky=(tk.W, tk.E))
        
        browse_btn = ttk.Button(folder_frame, text="Browse", command=self.browse_folder)
        browse_btn.grid(row=0, column=1)
        
        # Control buttons
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=2, column=0, pady=10)
        
        self.start_btn = ttk.Button(control_frame, text="Start Monitoring", 
                                    command=self.start_monitoring, width=15)
        self.start_btn.grid(row=0, column=0, padx=5)
        
        self.stop_btn = ttk.Button(control_frame, text="Stop Monitoring", 
                                   command=self.stop_monitoring, state='disabled', width=15)
        self.stop_btn.grid(row=0, column=1, padx=5)
        
        organize_btn = ttk.Button(control_frame, text="Organize Now", 
                                 command=self.organize_existing, width=15)
        organize_btn.grid(row=0, column=2, padx=5)
        
        undo_btn = ttk.Button(control_frame, text="Undo Last", 
                             command=self.undo_last, width=15)
        undo_btn.grid(row=0, column=3, padx=5)
        
        stats_btn = ttk.Button(control_frame, text="View Stats", 
                              command=self.show_stats, width=15)
        stats_btn.grid(row=0, column=4, padx=5)
        
        # Log area
        log_frame = ttk.LabelFrame(main_frame, text="Activity Log", padding="10")
        log_frame.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=15, width=70)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, 
                              relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=(5, 0))
        
        self.log("Smart File Sorter initialized!")
        self.log("Select a folder and click 'Start Monitoring' to begin.")
    
    def log(self, message):
        """Add a message to the log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
    
    def browse_folder(self):
        """Open folder browser dialog"""
        folder = filedialog.askdirectory()
        if folder:
            self.folder_var.set(folder)
    
    def start_monitoring(self):
        """Start monitoring the selected folder"""
        folder = self.folder_var.get()
        
        if not folder or not os.path.exists(folder):
            messagebox.showerror("Error", "Please select a valid folder!")
            return
        
        self.config.watched_folder = folder
        self.config.save_config()
        
        # Start file watcher
        event_handler = FileWatcher(self.organizer, folder, self.log)
        self.observer = Observer()
        self.observer.schedule(event_handler, folder, recursive=False)
        self.observer.start()
        
        self.watching = True
        self.start_btn.config(state='disabled')
        self.stop_btn.config(state='normal')
        self.status_var.set(f"Monitoring: {folder}")
        self.log(f"Started monitoring: {folder}")
    
    def stop_monitoring(self):
        """Stop monitoring the folder"""
        if self.observer:
            self.observer.stop()
            self.observer.join()
            self.observer = None
        
        self.watching = False
        self.start_btn.config(state='normal')
        self.stop_btn.config(state='disabled')
        self.status_var.set("Monitoring stopped")
        self.log("Stopped monitoring")
    
    def organize_existing(self):
        """Organize all existing files in the folder"""
        folder = self.folder_var.get()
        
        if not folder or not os.path.exists(folder):
            messagebox.showerror("Error", "Please select a valid folder!")
            return
        
        self.log("Organizing existing files...")
        count = 0
        
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            if os.path.isfile(file_path):
                result = self.organizer.organize_file(file_path, folder)
                if result:
                    count += 1
                    self.log(f"Organized: {filename}")
        
        self.log(f"Organized {count} files!")
        messagebox.showinfo("Success", f"Organized {count} files!")
    
    def undo_last(self):
        """Undo the last file move"""
        success, message = self.organizer.undo_last_move()
        if success:
            self.log(f"Undo successful: {message}")
        else:
            self.log(f"Undo failed: {message}")
            messagebox.showwarning("Undo Failed", message)
    
    def show_stats(self):
        """Show organization statistics"""
        stats = self.organizer.get_stats()
        
        if not stats:
            messagebox.showinfo("Statistics", "No files have been organized yet!")
            return
        
        stats_window = tk.Toplevel(self.root)
        stats_window.title("Organization Statistics")
        stats_window.geometry("400x300")
        
        # Set icon for stats window too
        try:
            icon_path = resource_path("app_icon.ico")
            stats_window.iconbitmap(icon_path)
        except:
            pass
        
        ttk.Label(stats_window, text="Files Organized by Category", 
                 font=('Arial', 12, 'bold')).pack(pady=10)
        
        # Create a treeview for stats
        tree = ttk.Treeview(stats_window, columns=('Category', 'Count'), 
                           show='headings', height=10)
        tree.heading('Category', text='Category')
        tree.heading('Count', text='Files')
        tree.column('Category', width=200)
        tree.column('Count', width=100)
        
        total = 0
        for category, count in sorted(stats.items(), key=lambda x: x[1], reverse=True):
            tree.insert('', tk.END, values=(category, count))
            total += count
        
        tree.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        ttk.Label(stats_window, text=f"Total Files Organized: {total}", 
                 font=('Arial', 10, 'bold')).pack(pady=5)

    def on_closing(self):
        """Handle window closing - stops monitoring and exits completely"""
        self.is_closing = True
        
        # Stop monitoring if active
        if self.observer:
            try:
                self.observer.stop()
                self.observer.join(timeout=2)
            except:
                pass
        
        # Stop tray icon
        if self.tray_icon:
            try:
                self.tray_icon.stop()
            except:
                pass
        
        # Cleanup lock file
        cleanup_lock()
        
        # Destroy the window and exit
        try:
            self.root.quit()
            self.root.destroy()
        except:
            pass


def main():
    """Main entry point"""
    # Check if another instance is already running
    if is_already_running():
        messagebox.showerror(
            "Already Running", 
            "Smart File Sorter is already running!\n\nCheck your system tray or task manager."
        )
        return
    
    # Register cleanup on exit
    import atexit
    atexit.register(cleanup_lock)
    
    root = tk.Tk()
    app = SmartFileSorterGUI(root)
    
    # Start tray icon in separate thread
    app.tray_thread = threading.Thread(target=app.setup_tray, daemon=True)
    app.tray_thread.start()
    
    # Give tray thread a moment to start
    time.sleep(0.5)
    
    root.mainloop()


if __name__ == "__main__":
    main()