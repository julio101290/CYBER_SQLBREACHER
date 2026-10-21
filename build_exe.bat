@echo off
setlocal
cd /d "%~dp0"
title COMPILADOR CYBER_SQL // GENERADOR EXE

echo ===================================================
echo  CYBER_SQL // COMPILADOR DE EJECUTABLE WINDOWS
echo ===================================================

:: 1. Verificar PyInstaller
pip show pyinstaller >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo [*] Instalando PyInstaller...
    pip install pyinstaller
)

:: 2. Limpieza de compilaciones previas
if exist "build" rd /s /q "build"
if exist "dist" rd /s /q "dist"
if exist "CyberSQLInjector.spec" del "CyberSQLInjector.spec"

:: 3. Compilar con PyInstaller en un único archivo (--onefile) y sin consola negra (--windowed)
echo [*] Compilando CyberSQLInjector.exe...
pyinstaller --noconfirm --onefile --windowed ^
    --name "CyberSQLInjector" ^
    --collect-all tkinter ^
    cyber_import.py

if %ERRORLEVEL% equ 0 (
    echo.
    echo ===================================================
    echo  [OK] Compilacion finalizada con exito!
    echo  Ubicacion: dist\CyberSQLInjector.exe
    echo ===================================================
) else (
    echo.
    echo  [!] Hubo un error durante la compilacion.
)

pause
