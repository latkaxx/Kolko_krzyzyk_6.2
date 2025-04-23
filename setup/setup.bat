@echo off
setlocal

REM Try to find python
where python >nul 2>&1
if errorlevel 1 (
    REM Try python3
    where python3 >nul 2>&1
    if errorlevel 1 (
        echo Python is not installed on this system.
        exit /b 1
    ) else (
        set "PYTHON=python3"
    )
) else (
    set "PYTHON=python"
)

REM Create virtual environment
%PYTHON% -m venv env
if errorlevel 1 (
    echo Failed to create virtual environment.
    exit /b 1
)

REM Activate virtual environment
call env\Scripts\activate.bat

REM Install dependencies
pip install -r requirements.txt
if errorlevel 1 (
    echo Failed to install dependencies.
    exit /b 1
)

endlocal

