# 🗂️ Smart File Sorter

An intelligent, automated file organization tool that monitors folders and sorts files by type with advanced features like duplicate detection, undo functionality, and statistics tracking. Built with Python and available as a standalone executable.

![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows-blue.svg)

## ✨ Features

### Core Functionality

- 📁 **Automatic File Monitoring**: Real-time monitoring of folders with instant file organization
- 🎯 **Smart Categorization**: Automatically sorts files into categories (Images, Documents, Videos, Audio, etc.)
- 🔄 **Manual Organization**: Organize existing files with a single click
- 💾 **Persistent Configuration**: Saves your preferences and folder settings
- 🖥️ **System Tray Integration**: Minimize to system tray and manage from there

### Advanced Features (Portfolio Highlights!)

- 🔍 **Duplicate Detection**: Identifies duplicate files using MD5 hashing and moves them to a separate folder
- ⏮️ **Undo Functionality**: Reverse any file move operation with full history tracking (up to 100 operations)
- 📊 **Statistics Dashboard**: View detailed analytics about organized files
- 🎨 **User-Friendly GUI**: Clean, intuitive interface built with tkinter
- ⚙️ **Customizable Categories**: Easily modify file type categories and extensions
- 🚫 **Single Instance Protection**: Prevents multiple instances from running simultaneously

## 🚀 Quick Start

### Option 1: Download & Run Executable (Easiest)

1. Download the installer from the releases page
2. Run the installer and follow the prompts
3. Launch "Smart File Sorter" from your Start Menu

### Option 2: Run from Python Source

1. **Install Python 3.7 or higher** from [python.org](https://www.python.org)

2. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**
   ```bash
   python Smart_File_Sorter.py
   ```

## 📖 Detailed Usage Guide

### Getting Started

1. **Launch the Application**
   - If installed: Click "Smart File Sorter" in Start Menu
   - If running from source: `python Smart_File_Sorter.py`

2. **Select a Folder**
   - Click the "Browse" button
   - Choose the folder you want to monitor
   - The folder path will be saved for future sessions

3. **Start Monitoring**
   - Click "Start Monitoring" to begin automatic file organization
   - Any new files added to the folder will be automatically sorted
   - Click "Stop Monitoring" to pause monitoring
   - Minimize to system tray to keep it running in the background

4. **Organize Existing Files**
   - Click "Organize Now" to sort all files currently in the folder
   - Useful for cleaning up existing clutter

### Advanced Features

#### Undo Last Action

- Click "Undo Last" to reverse the most recent file move
- Up to 100 operations are tracked in history
- History persists between sessions
- Full path recovery maintained

#### View Statistics

- Click "View Stats" to see:
  - Number of files organized by category
  - Total files processed
  - Category distribution chart

#### Duplicate Detection

- **Enabled by default**
- Automatic MD5 hash comparison
- Duplicate files moved to "Duplicates" folder
- Prevents duplicate organization

#### System Tray

- Minimize to system tray
- Quick access menu:
  - Show Window
  - Start/Stop Monitoring
  - Exit Application

## 📂 File Categories

The application organizes files into these default categories:

| Category        | File Extensions                                               |
| --------------- | ------------------------------------------------------------- |
| **Images**      | .jpg, .jpeg, .png, .gif, .bmp, .svg, .webp, .ico, .tiff       |
| **Documents**   | .pdf, .doc, .docx, .txt, .rtf, .odt, .xls, .xlsx, .ppt, .pptx |
| **Videos**      | .mp4, .avi, .mkv, .mov, .wmv, .flv, .webm, .m4v               |
| **Audio**       | .mp3, .wav, .flac, .aac, .ogg, .wma, .m4a                     |
| **Archives**    | .zip, .rar, .7z, .tar, .gz, .bz2, .xz                         |
| **Code**        | .py, .js, .html, .css, .java, .cpp, .c, .h, .json, .xml, .sql |
| **Executables** | .exe, .msi, .app, .dmg, .deb, .rpm                            |
| **Others**      | All other file types                                          |
| **Duplicates**  | Auto-generated for duplicate files                            |

### Customizing Categories

Edit the `config.json` file (created after first run) in your AppData folder:

```json
{
  "categories": {
    "Images": [".jpg", ".jpeg", ".png"],
    "MyCustomCategory": [".xyz", ".abc"],
    "Documents": [".pdf", ".doc", ".docx", ".txt"]
  },
  "watched_folder": "C:\\Users\\YourName\\Downloads",
  "enable_duplicates": true,
  "enable_undo": true
}
```

## 🏗️ Project Structure

```
Smart_File_Sorter/
│
├── Smart_File_Sorter.py        # Main application (source code)
├── SmartFileSorter.spec        # PyInstaller configuration
├── requirements.txt            # Python dependencies
├── build_installer.bat         # Batch script to build installer
├── installer_script.iss        # Inno Setup installer script
│
├── README.md                   # Original README
├── README1.md                  # Comprehensive README (this file)
├── QUICKSTART.md              # Quick start guide
├── PORTFOLIO_GUIDE.md         # Portfolio highlights
├── LICENSE                    # MIT License
├── config.json                # Auto-generated (user config)
├── history.json               # Auto-generated (undo history)
│
├── build/                     # PyInstaller build output
│   └── SmartFileSorter/
│       ├── SmartFileSorter.exe
│       ├── Various .toc and .pyz files
│       └── localpycs/
│
└── installer_output/          # Inno Setup installer output
    └── SmartFileSorterSetup.exe
```

## 🛠️ Building & Distribution

### Building the Executable (PyInstaller)

**Prerequisites:**

- Python 3.7+
- All dependencies from `requirements.txt`

**Build Steps:**

1. **Install PyInstaller** (included in requirements.txt)

   ```bash
   pip install -r requirements.txt
   ```

2. **Build the executable**

   ```bash
   pyinstaller SmartFileSorter.spec
   ```

   Or manually:

   ```bash
   pyinstaller --onefile --windowed --icon=app_icon.ico Smart_File_Sorter.py
   ```

3. **Output**
   - Executable: `build/SmartFileSorter/SmartFileSorter.exe`
   - Distributable: Place the entire `SmartFileSorter/` folder

### Building the Installer (Inno Setup)

**Prerequisites:**

- Inno Setup 6.0+ (free download from [innosetup.com](https://jrsoftware.org/isdl.php))
- PyInstaller executable already built

**Build Steps:**

1. **Using the batch script**

   ```bash
   build_installer.bat
   ```

2. **Or manually with Inno Setup**
   - Open `installer_script.iss` in Inno Setup
   - Click "Build" → "Compile"
   - Output: `installer_output/SmartFileSorterSetup.exe`

3. **Installer Features**
   - Automatic .exe installation
   - Start Menu shortcuts
   - Add/Remove Programs entry
   - Optional desktop shortcut
   - Uninstall capability

## 🔧 Technical Architecture

### Architecture Overview

The application is built with a modular, object-oriented design:

1. **Config Class**: Manages configuration and persistence
   - Loads/saves settings to JSON
   - Manages category definitions
   - Tracks folder preferences

2. **FileOrganizer Class**: Core sorting logic
   - File categorization based on extensions
   - Duplicate detection using MD5 hashing
   - Operation history tracking
   - Statistics collection

3. **FileWatcher Class**: Real-time file system monitoring
   - Inherits from `watchdog.FileSystemEventHandler`
   - Monitors file creation events
   - Prevents duplicate processing
   - Adds processing delay for file stability

4. **SmartFileSorterGUI Class**: User interface
   - Built with tkinter framework
   - Folder selection dialog
   - Real-time activity logging
   - Statistics window
   - System tray integration

### Key Dependencies

- **watchdog (3.0.0)**: File system event monitoring
- **tkinter**: Cross-platform GUI framework (bundled with Python)
- **pystray (0.19.5)**: System tray functionality
- **Pillow (10.1.0)**: Image handling for icons
- **psutil (5.9.6)**: Process monitoring and management
- **pyinstaller (6.1.0)**: Executable building (development only)

### How It Works (Process Flow)

```
User Input
    ↓
File Created/Added
    ↓
FileWatcher detects event
    ↓
Get file extension
    ↓
Determine category
    ↓
Check for duplicates (MD5 hash)
    ↓
Create category folder if needed
    ↓
Handle filename conflicts
    ↓
Move file
    ↓
Record in history
    ↓
Update statistics
    ↓
Log activity
```

## 🎯 Portfolio Highlights

This project demonstrates advanced software engineering practices:

- ✅ **Clean Code Architecture**: Modular, object-oriented design with single responsibility principle
- ✅ **GUI Development**: Professional interface with tkinter, threading, and system integration
- ✅ **File System Operations**: Safe, robust file handling with error recovery
- ✅ **Data Persistence**: JSON-based configuration and comprehensive history tracking
- ✅ **Error Handling**: Comprehensive exception handling with user-friendly messages
- ✅ **User Experience**: Intuitive interface with real-time feedback and activity logging
- ✅ **Advanced Features**: Duplicate detection, undo functionality, statistics tracking
- ✅ **Background Operations**: Threading and system tray integration
- ✅ **Deployment**: PyInstaller and Inno Setup configuration for distribution
- ✅ **Code Quality**: Well-documented, commented code with clear function signatures

## 🔍 Configuration Files

### config.json (Auto-Generated)

Location: `C:\Users\YourName\AppData\Roaming\SmartFileSorter\config.json`

```json
{
  "categories": {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp"],
    "Documents": [".pdf", ".doc", ".docx", ".txt"],
    "Videos": [".mp4", ".avi", ".mkv"],
    "Audio": [".mp3", ".wav", ".flac"],
    "Archives": [".zip", ".rar", ".7z"],
    "Code": [".py", ".js", ".html", ".css"],
    "Executables": [".exe", ".msi"],
    "Others": []
  },
  "watched_folder": "C:\\Users\\YourName\\Downloads",
  "enable_duplicates": true,
  "enable_undo": true
}
```

### history.json (Auto-Generated)

Tracks up to 100 file move operations for undo functionality.

## 🐛 Troubleshooting

### Common Issues & Solutions

| Issue                                  | Solution                                                                                             |
| -------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| **Application won't start**            | Ensure Python 3.7+ is installed; reinstall dependencies: `pip install -r requirements.txt --upgrade` |
| **Files not organizing automatically** | Check that "Start Monitoring" is active; verify folder path is valid and accessible                  |
| **Permission errors**                  | Run as Administrator; ensure you have write permissions to the target folder                         |
| **Undo not working**                   | Check that "enable_undo" is true in config.json; history file may be corrupted                       |
| **Duplicate detection not working**    | Verify "enable_duplicates" is true in config.json                                                    |
| **Multiple instances running**         | Check system tray; use Task Manager to close all instances; delete lock file in AppData              |
| **Installer won't run**                | Ensure Inno Setup 6.0+ is installed; check build_installer.bat script                                |

### Debug Mode

Run from command prompt to see error messages:

```bash
python Smart_File_Sorter.py
```

Check logs in activity window for detailed operation information.

## 🔄 Future Enhancements

Potential features for version 2.0:

- 🌐 Cloud storage integration (Google Drive, OneDrive, Dropbox)
- 🤖 Machine learning-based file classification
- 📅 Date-based organization options (by year, month)
- 🔔 Desktop notifications for organized files
- 📝 Custom file naming rules with regex support
- 🌍 Multi-language support (internationalization)
- 🎨 Dark mode and customizable themes
- 📦 Auto-update functionality
- 🔐 Backup and restore settings
- 📱 Mobile companion app

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

### MIT License Summary

- ✅ Commercial use
- ✅ Modification
- ✅ Distribution
- ✅ Private use
- ❌ Liability
- ❌ Warranty

## 👤 Author

**Anurag Wanwe**

- GitHub: [@Deathblu](https://github.com/Deathblu)
- LinkedIn: [Anurag Wanwe](https://linkedin.com/in/anurag-wanwe-17b8ab243)
- Email: [anuwanwe1463@gmail.com](mailto:anuwanwe1463@gmail.com)

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## ⭐ Show Your Support

If this project helped you, please consider:

- ⭐ Giving it a star on GitHub
- 📣 Sharing it with others
- 💬 Providing feedback

## 📧 Contact & Support

For questions, feedback, or support:

- **Email**: [anuwanwe1463@gmail.com](mailto:anuwanwe1463@gmail.com)
- **GitHub Issues**: Report bugs and request features
- **GitHub Discussions**: General questions and discussions

## 📚 Additional Resources

- [Python Documentation](https://docs.python.org/)
- [Watchdog Documentation](https://watchdog.readthedocs.io/)
- [Tkinter Documentation](https://docs.python.org/3/library/tkinter.html)

---

**Note**: This is a professional portfolio project designed to showcase Python development skills, GUI design, file system operations, and software engineering best practices. It is production-ready and fully functional.

**Last Updated**: February 6, 2026
**Version**: 1.0
