@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>&1
if errorlevel 1 (
 echo Please install Python 3 from https://www.python.org/downloads/windows/
 pause
 exit /b 1
)
py -m pip install -r requirements.txt
if errorlevel 1 goto failed
py -m PyInstaller --noconfirm --clean --onefile --windowed --name "Markdown转PDF" --collect-all weasyprint --collect-all markdown --collect-all pygments gui.py
if errorlevel 1 goto failed
echo.
echo EXE location: dist\Markdown转PDF.exe
echo IMPORTANT: Test on a clean Windows PC. WeasyPrint may require additional native libraries.
pause
exit /b 0
:failed
echo Build failed. Check Python, pip and WeasyPrint native dependencies.
pause
exit /b 1
