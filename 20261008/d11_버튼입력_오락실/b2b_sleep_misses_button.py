from machine import Pin
import time

btn = Pin(0, Pin.IN, Pin.PULL_UP)       # 누르면 0
flash = Pin(4, Pin.OUT, value=0)        # 플래시: 매우 밝다, 직시 금지

count = 0       # 버튼 눌림 횟수
btn_last = 1    # 직전에 읽은 버튼 값

# 일부러 놓친다: sleep 으로 500ms 씩 잠들어 있는 동안에는 버튼을 볼 수 없다.
# 짧게 "톡" 누르면 잠든 사이에 눌렀다 떼서 아예 못 본다.
# 실제로 10번 눌러 보고, 화면에 찍히는 횟수와 비교해 보자.

def check_button():
    global count, btn_last
    now = btn.value()
    if btn_last == 1 and now == 0:   # 뗀 상태에서 누른 상태로 바뀐 순간
        count += 1
        print("눌림 감지! 지금까지", count, "번")
    btn_last = now

try:
    while True:
        flash.value(1)
        time.sleep_ms(500)    # 이 500ms 동안 버튼은 안 보인다
        check_button()
        flash.value(0)
        time.sleep_ms(500)    # 여기서도 안 보인다
        check_button()
except KeyboardInterrupt:
    flash.value(0)
    print("종료. 감지된 횟수:", count)

# ⭐ 도전: sleep_ms(500) 을 sleep_ms(50) 으로 줄이면 얼마나 덜 놓칠까? 그래도 놓치는 순간이 있을까?
