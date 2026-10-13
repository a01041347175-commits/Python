# ESP32-CAM 카메라 포함 MicroPython 펌웨어

- 파일: `firmware_AI_THINKER_mpy1.27.0.bin` (1,808,576 바이트)
- 출처: https://github.com/cnadler86/micropython-camera-API/releases (v0.6.2, 2026-01-12) 의 `mpy_cam-v1.27.0-AI_THINKER.zip` 안 `firmware.bin` 을 그대로 옮겼다.
- 기반: MicroPython 1.27.0, 빌드 `ESP32_GENERIC-SPIRAM`, 카메라 모듈 `camera` 포함.
- 올리는 주소: **0x1000** (Thonny 의 Target address 기본값이 ESP32 에서는 0x1000)
- 강사 보드 실측(2026-10-08): 부팅 → `import camera` 성공 → JPEG 사진 · Wi-Fi 웹 서버 스트리밍 · 블루투스 모두 동작.
- 원래(일반) 펌웨어로 되돌리려면 `펌웨어_원복.bat` 더블클릭. 올라가는 파일은 `esp32_generic_mpy1.29.0.bin` (MicroPython 공식 `ESP32_GENERIC-20260824-v1.29.0.bin`, 1,790,544 바이트, 주소 0x1000).
- 원복 실측(2026-10-11, 맥북 + ESP32-CAM-MB): 같은 esptool 명령(`--erase-all -z 0x1000`, 460800 baud)으로 지우기 13.3초 → 쓰기 32.5초 → `Hash of data verified.` → 부팅 줄 `MicroPython v1.29.0 ... Generic ESP32 module with ESP32`(SPIRAM 없음), `import camera` 는 `ImportError`.
- `펌웨어_원복.bat` 은 윈도우 PC 에서 아직 실행해 보지 않았다(굽기 bat 와 파일 이름·문구만 다르다).
