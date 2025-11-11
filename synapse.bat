@echo off
setlocal enabledelayedexpansion

title Synapse Interpreter

echo ========================================
echo        Synapse Language v1.0
echo ========================================
echo.

set "FILE=%~1"
set "EXT=%~x1"

if "!FILE!"=="" (
    echo [ERROR] Any File expecified.
    goto :fim
)

if not exist "!FILE!" (
    echo [ERRO] File "!FILE!" not found.
    goto :fim
)

echo Executing: !FILE!
echo ========================================
echo.

REM Executa o interpretador
python index.py "!FILE!"

if !errorlevel! neq 0 (
    echo.
    echo ========================================
)

:fim
echo.
echo Press any key to close...
pause > nul