from machine import Pin
import time

btn = Pin(0, Pin.IN, Pin.PULL_UP)  # IO0 버튼: 안 누르면 1, 누르면 0

last = btn.value()
print("시작 상태:", last)

try:
    while True:
        now = btn.value()
        if now != last:
            if now == 0:
                print("눌림 (0)")
            else:
                print("뗌 (1)")
            last = now
        time.sleep_ms(10)
except KeyboardInterrupt:
    print("종료")
