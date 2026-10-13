# 보드가 main.py 를 혼자 돌리고 있어서 Thonny 가 연결을 못 할 때 쓰는 구조 스크립트
# ★ 이 파일은 보드가 아니라 '컴퓨터'에서 돌린다 → Thonny 오른쪽 아래에서 "Local Python 3" 를 고른 뒤 ▶ 실행
import time
import serial
import serial.tools.list_ports

# 1) 보드 찾기: 보드의 USB 칩(CH340 · CP210x · FTDI)이 꽂힌 포트
CHIPS = (0x1A86, 0x10C4, 0x0403)
ports = [p.device for p in serial.tools.list_ports.comports() if p.vid in CHIPS]
if not ports:
    raise SystemExit("보드를 못 찾았어요. USB 선(충전 전용 아님)을 다시 꽂고 다시 실행하세요.")
port = ports[0]
print("보드 포트:", port)

# 2) 포트를 연다 (이때 보드가 한 번 다시 시작된다) → 부팅이 끝나길 기다린다
s = serial.Serial(port, 115200, timeout=0.2)
s.dtr = False
s.rts = True            # 보드를 한 번 확실히 다시 시작
time.sleep(0.1)
s.rts = False
time.sleep(1.5)         # 부팅 직후의 Ctrl+C 는 사라진다 → 1.5초 기다린 뒤에 보낸다
s.read(5000)

# 3) Ctrl+C 를 보내 main.py 를 멈춘다 → >>> 가 보일 때까지
ok = False
for _ in range(10):
    s.write(b"\x03")
    time.sleep(0.4)
    if b">>>" in s.read(5000):
        ok = True
        break
if not ok:
    s.close()
    raise SystemExit("멈추지 못했어요. 보드의 RESET 버튼을 한 번 누르고 다시 실행하세요.")
print("멈춤 성공 (>>> 확인)")

# 4) main.py 가 있으면 지운다
def ask(cmd):
    s.write(cmd.encode() + b"\r\n")
    time.sleep(0.5)
    return s.read(5000).decode("utf-8", "ignore")

ask("import os")
print("지우기 전 파일:", ask("print(os.listdir())").split("\n")[1].strip())
ask("os.remove('main.py') if 'main.py' in os.listdir() else None")
print("지운 뒤 파일:", ask("print(os.listdir())").split("\n")[1].strip())
s.close()
print("끝! 이제 오른쪽 아래를 'MicroPython (ESP32)' 로 되돌리고 보드의 RESET 을 눌러 연결하세요.")
