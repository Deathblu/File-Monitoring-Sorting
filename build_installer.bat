@echo off
REM Complete Build Script for Smart File Sorter
REM Builds both the executable AND the installer in one go

echo ==========================================
echo   Smart File Sorter - Complete Build
echo ==========================================
echo.
echo This script will:
echo 1. Create icons if missing
echo 2. Build the executable with PyInstaller
echo 3. Create the Windows installer with Inno Setup
echo.
pause
echo.

REM ==========================================
REM STEP 1: Environment Checks
REM ==========================================

echo [STEP 1/8] Checking environment...
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)
echo ✓ Python found

REM Check Inno Setup
set INNO_PATH="C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
if not exist %INNO_PATH% (
    echo.
    echo [WARNING] Inno Setup not found!
    echo.
    echo To create the installer, you need Inno Setup 6.
    echo Download from: https://jrsoftware.org/isdl.php
    echo.
    echo You can continue to build just the .exe file,
    echo or press Ctrl+C to cancel and install Inno Setup first.
    echo.
    pause
    set BUILD_INSTALLER=0
) else (
    echo ✓ Inno Setup found
    set BUILD_INSTALLER=1
)

echo.
echo ==========================================
echo [STEP 2/8] Checking/Creating Icons
echo ==========================================
echo.

REM Check for icons
if not exist "app_icon.ico" (
    echo app_icon.ico not found, creating placeholder...
    python create_placeholder_icons.py
    if errorlevel 1 (
        echo [ERROR] Failed to create icons
        echo Make sure Pillow is installed: pip install Pillow
        pause
        exit /b 1
    )
) else (
    echo ✓ app_icon.ico found
)

if not exist "tray_icon.ico" (
    echo tray_icon.ico not found, creating placeholder...
    python create_placeholder_icons.py
    if errorlevel 1 (
        echo [ERROR] Failed to create icons
        pause
        exit /b 1
    )
) else (
    echo ✓ tray_icon.ico found
)

echo.
echo ==========================================
echo [STEP 3/8] Installing Python Dependencies
echo ==========================================
echo.

pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo Installing PyInstaller...
pip install pyinstaller
if errorlevel 1 (
    echo [ERROR] Failed to install PyInstaller
    pause
    exit /b 1
)

echo ✓ Dependencies installed

echo.
echo ==========================================
echo [STEP 4/8] Cleaning Previous Builds
echo ==========================================
echo.

if exist build (
    echo Removing old build folder...
    rmdir /s /q build
)

if exist dist (
    echo Removing old dist folder...
    rmdir /s /q dist
)

if exist __pycache__ (
    echo Removing __pycache__...
    rmdir /s /q __pycache__
)

if exist installer_output (
    echo Removing old installer output...
    rmdir /s /q installer_output
)

echo ✓ Cleanup complete

echo.
echo ==========================================
echo [STEP 5/8] Building Executable
echo ==========================================
echo.

echo Running PyInstaller...
pyinstaller SmartFileSorter.spec --clean
if errorlevel 1 (
    echo.
    echo [ERROR] PyInstaller build failed!
    echo Check the output above for errors.
    pause
    exit /b 1
)

echo.
echo ==========================================
echo [STEP 6/8] Verifying Executable
echo ==========================================
echo.

if not exist "dist\SmartFileSorter.exe" (
    echo [ERROR] SmartFileSorter.exe not found in dist folder!
    pause
    exit /b 1
)

echo ✓ Executable created successfully

REM Get file size
for %%A in ("dist\SmartFileSorter.exe") do set size=%%~zA
set /a sizeInMB=%size%/1048576
echo ✓ File size: %sizeInMB% MB

echo.
echo ==========================================
echo [STEP 7/8] Preparing Installer Files
echo ==========================================
echo.

REM Check for README and LICENSE
if not exist "README.txt" (
    echo [WARNING] README.txt not found
    echo The installer will work but won't include a README
) else (
    echo ✓ README.txt found
)

if not exist "LICENSE.txt" (
    echo [WARNING] LICENSE.txt not found
    echo The installer will work but won't include a LICENSE
) else (
    echo ✓ LICENSE.txt found
)

echo.
echo ==========================================
echo [STEP 8/8] Building Installer
echo ==========================================
echo.

if %BUILD_INSTALLER%==1 (
    echo Creating Windows installer with Inno Setup...
    echo.
    
    if not exist "installer_script.iss" (
        echo [ERROR] installer_script.iss not found!
        echo Cannot create installer without the Inno Setup script.
        pause
        exit /b 1
    )
    
    %INNO_PATH% installer_script.iss
    if errorlevel 1 (
        echo.
        echo [ERROR] Installer creation failed!
        echo Check the Inno Setup output above for errors.
        echo.
        echo The executable is still available in dist\SmartFileSorter.exe
        pause
        exit /b 1
    )
    
    echo.
    echo ✓ Installer created successfully!
    
    REM Check installer file
    for %%F in (installer_output\SmartFileSorter_Setup_*.exe) do (
        set INSTALLER_FILE=%%F
        for %%A in ("%%F") do set INSTALLER_SIZE=%%~zA
    )
    
    if defined INSTALLER_FILE (
        set /a installerSizeInMB=%INSTALLER_SIZE%/1048576
        echo ✓ Installer: !INSTALLER_FILE!
        echo ✓ Installer size: !installerSizeInMB! MB
    )
) else (
    echo [SKIPPED] Inno Setup not available
    echo Installer was not created.
    echo.
    echo To create an installer:
    echo 1. Install Inno Setup from https://jrsoftware.org/isdl.php
    echo 2. Run this script again
)

echo.
echo ==========================================
echo           BUILD COMPLETE! 
echo ==========================================
echo.

if %BUILD_INSTALLER%==1 (
    echo ✓ Executable: dist\SmartFileSorter.exe
    echo ✓ Installer:  installer_output\SmartFileSorter_Setup_v1.0.0.exe
    echo.
    echo You can now distribute the installer to users!
    echo.
    echo The installer will:
    echo - Install to Program Files
    echo - Create Start Menu shortcut
    echo - Optionally create Desktop shortcut
    echo - Include uninstaller
    echo.
) else (
    echo ✓ Executable: dist\SmartFileSorter.exe
    echo.
    echo Note: Installer was not created (Inno Setup not found)
    echo You can still distribute the .exe file directly.
    echo.
)

echo ==========================================
echo.
echo Next steps:
echo 1. Test the executable: dist\SmartFileSorter.exe

if %BUILD_INSTALLER%==1 (
    echo 2. Test the installer: installer_output\SmartFileSorter_Setup_v1.0.0.exe
    echo 3. Distribute the installer to your users
) else (
    echo 2. Distribute the .exe file
    echo    OR install Inno Setup and run this script again
)

echo.
pause
