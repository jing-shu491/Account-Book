@echo off
chcp 65001 >nul
cd /d "%~dp0"
where py >nul 2>nul
if %errorlevel% equ 0 (
  py -3 launch.py
) else (
  where python >nul 2>nul
  if errorlevel 1 (
    echo 请先安装 Python 3.9 或以上版本，并勾选 Add Python to PATH。
    echo 下载地址：https://www.python.org/downloads/windows/
    pause
    exit /b 1
  )
  python launch.py
)
pause
