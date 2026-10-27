import machine
import time
from machine import Pin, PWM

buzzer = PWM(Pin(6), freq=880, duty=0)
trigger = Pin(17, mode=Pin.OUT, pull=None)
echo = Pin(1, mode=Pin.IN, pull=None)
trigger.value(0)

# ---- 내가 바꾸는 값 : r2_거리_범위재기.py 로 잰 내 값을 넣는다 ----
NEAR_CM = 5                      # 이 거리 이하면 소리가 쭉 이어진다 (연속음)
FAR_CM = 40                      # 이 거리 이상이면 가장 짧고 빠른 삑 : NEAR_CM 보다 커야 한다
LEVELS = 20                      # 거리를 몇 단계로 나눌까 (3 이상)
VOLUME = 10                      # 소리 크기 : 거리와 상관없이 항상 이 값 (10 ~ 512, 512 가 가장 큼)
BEEP_MIN_MS = 40                 # 가장 멀 때 삑 길이 (짧게)
BEEP_MAX_MS = 600                # 연속음 바로 앞 단계의 삑 길이 (길게)
REST_MS = 100                    # 삑과 삑 사이 쉬는 시간 : 항상 같다
LOOK_MS = 50                     # 연속음일 때 센서를 다시 보는 간격

def get_distance_cm():           # 교재 5-3 _2 와 같은 함수 : 못 읽으면 0
    trigger.value(0)
    time.sleep_us(5)
    trigger.value(1)
    time.sleep_us(10)
    trigger.value(0)
    pulse_time = machine.time_pulse_us(echo, 1, 30000)
    distance_cm = (pulse_time / 2) / 29.1
    if 2 <= distance_cm <= 200:
        return distance_cm
    else:
        return 0

def distance_level(cm):
    # 가까울수록 큰 단계 : NEAR_CM 이하 -> 20, FAR_CM 이상 -> 1
    level = (FAR_CM - cm) * LEVELS // (FAR_CM - NEAR_CM) + 1
    return max(1, min(LEVELS, int(level)))

def beep_length(level):
    # 단계 1 -> BEEP_MIN_MS (짧게), 단계 19 -> BEEP_MAX_MS (길게)
    return BEEP_MIN_MS + (level - 1) * (BEEP_MAX_MS - BEEP_MIN_MS) // (LEVELS - 2)

level = 1                        # 처음 단계 : 가장 먼 것으로 시작

try:
    while True:
        cm = get_distance_cm()
        if cm != 0:                              # 0 은 못 읽은 것 : 이전 단계를 그대로 쓴다
            level = distance_level(cm)

        if level == LEVELS:                      # 가장 가까움 : 끄지 않고 쭉 켜 둔다
            buzzer.duty(VOLUME)
            print("거리", int(cm), "cm -> 단계", level, "-> 연속음")
            time.sleep_ms(LOOK_MS)               # 잠깐만 기다리고 바로 센서를 다시 본다
        else:                                    # 그 밖 : 삑 길이만 바뀌고 쉬는 시간은 같다
            beep_ms = beep_length(level)
            print("거리", int(cm), "cm -> 단계", level, "-> 삑", beep_ms, "ms + 쉼", REST_MS, "ms")
            buzzer.duty(VOLUME)
            time.sleep_ms(beep_ms)
            buzzer.duty(0)
            time.sleep_ms(REST_MS)
except KeyboardInterrupt:
    pass
finally:
    buzzer.duty(0)
    buzzer.deinit()