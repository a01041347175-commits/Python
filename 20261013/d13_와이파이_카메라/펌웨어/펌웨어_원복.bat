@echo off
setlocal
title ESP32-CAM firmware restore
echo ================================================
echo  ESP32-CAM firmware RESTORE - back to standard MicroPython
echo  1. Close Thonny     2. Plug in ONE board
echo ================================================
set "PY="
if exist "%LOCALAPPDATA%\Programs\Thonny\python.exe" set "PY=%LOCALAPPDATA%\Programs\Thonny\python.exe"
if not defined PY if exist "%ProgramFiles%\Thonny\python.exe" set "PY=%ProgramFiles%\Thonny\python.exe"
if not defined PY if exist "%ProgramFiles(x86)%\Thonny\python.exe" set "PY=%ProgramFiles(x86)%\Thonny\python.exe"
if not defined PY goto :nothonny
set "BIN=%~dp0esp32_generic_mpy1.29.0.bin"
if not exist "%BIN%" goto :nobin
set "PORT="
for /f "usebackq delims=" %%P in (`powershell -NoProfile -Command "$n=(Get-CimInstance Win32_PnPEntity | Where-Object { $_.Name -match 'CH340|CH9102|CP210|USB-SERIAL|USB Serial' -and $_.Name -match '[(]COM[0-9]+[)]' } | Select-Object -First 1).Name; if ($n -match '[(](COM[0-9]+)[)]') { $Matches[1] }"`) do set "PORT=%%P"
if not defined PORT goto :noport
echo Board port: %PORT%
echo Restoring... wait about 1 minute. Do not unplug.
"%PY%" -m esptool --chip esp32 --port %PORT% --baud 460800 write-flash --erase-all -z 0x1000 "%BIN%"
if errorlevel 1 goto :fail
echo.
echo ================================================
echo  DONE.  Press the RESET button on the board,
echo  then open Thonny.
echo ================================================
pause
exit /b 0

:nothonny
echo [ERROR] Thonny was not found on this PC.
goto :fail
:nobin
echo [ERROR] The firmware file is not next to this script.
goto :fail
:noport
echo [ERROR] Board port not found. Check the USB cable.
goto :fail
:fail
echo.
echo  FAILED. Read the message above and call the teacher.
pause
exit /b 1
