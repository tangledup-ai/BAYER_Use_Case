@echo off
chcp 65001 >nul

echo ========================================
echo   Bayer Scheduling System - Build Tool
echo ========================================
echo.

:: Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found. Please install Python 3.8+
    echo Download: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [1/5] Checking Python version...
python --version
echo.

:: Check PyInstaller installation
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo [2/5] Installing PyInstaller...
    pip install pyinstaller
    if errorlevel 1 (
        echo [ERROR] PyInstaller installation failed
        pause
        exit /b 1
    )
)
echo.

:: Install project dependencies
echo [3/5] Installing project dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Project dependencies installation failed
    pause
    exit /b 1
)
echo.

:: Clean old build files
echo [4/5] Cleaning old build files...
if exist "build" (
    rmdir /s /q build
)
if exist "dist" (
    rmdir /s /q dist
)
echo.

:: Build executable
echo [5/5] Starting build...
echo ========================================
pyinstaller build.spec --clean
echo ========================================
echo.

:: Check if build succeeded
if exist "dist\拜耳排班系统\拜耳排班系统.exe" (
    echo [SUCCESS] Build completed!
    echo.
    echo Executable location:
    echo %~dp0dist\拜耳排班系统\拜耳排班系统.exe
    echo.
    echo Next steps:
    echo 1. Navigate to: dist\拜耳排班系统\
    echo 2. Copy the entire folder to your Windows system
    echo 3. Double-click 拜耳排班系统.exe to run
    echo.
    set /p choice=Run test now? (Y/N):
    if /i "%choice%"=="Y" (
        start "" "dist\拜耳排班系统\拜耳排班系统.exe"
    )
) else (
    echo [FAILED] Build failed. Please check error messages above.
    echo.
    echo Common issues:
    echo 1. Ensure no Chinese characters in project path
    echo 2. Make sure port 5000 is not in use
    echo 3. Check error logs above
    echo 4. Verify all dependencies are installed
    echo.
    echo For detailed troubleshooting, see WINDOWS_BUILD_GUIDE.md
    pause
    exit /b 1
)

pause
