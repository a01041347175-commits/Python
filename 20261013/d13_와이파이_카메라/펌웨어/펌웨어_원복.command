#!/bin/bash
# ESP32-CAM firmware restore - generic version (Mac). Double-click this file.
# Thonny must be closed and ONE board plugged in.
cd "$(dirname "$0")" || exit 1
echo "================================================"
echo " ESP32-CAM firmware restore - generic version"
echo " 1. Close Thonny     2. Plug in ONE board"
echo "================================================"
PY="/Applications/Thonny.app/Contents/Frameworks/Python.framework/Versions/3.14/bin/python3.14"
BIN="$PWD/esp32_generic_mpy1.29.0.bin"
fail() { echo; echo " FAILED. Read the message above and call the teacher."; read -n 1 -s -r -p "Press any key to close."; exit 1; }
[ -x "$PY" ] || { echo "[ERROR] Thonny was not found in /Applications."; fail; }
[ -f "$BIN" ] || { echo "[ERROR] The firmware file is not next to this script."; fail; }
PORT=$("$PY" -I -c "
import serial.tools.list_ports as lp
c=[p.device for p in lp.comports() if p.vid in (0x1A86,0x10C4,0x0403) and 'cu.' in p.device]
print(c[0] if c else '')")
[ -n "$PORT" ] || { echo "[ERROR] Board port not found. Check the USB cable."; fail; }
echo "Board port: $PORT"
echo "Flashing... wait about 1 minute. Do not unplug."
"$PY" -I -m esptool --chip esp32 --port "$PORT" --baud 460800 write-flash --erase-all -z 0x1000 "$BIN" || fail
echo
echo "================================================"
echo " DONE.  Press the RESET button on the board,"
echo " then open Thonny."
echo "================================================"
read -n 1 -s -r -p "Press any key to close."
