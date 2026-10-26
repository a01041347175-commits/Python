from machine import Pin, PWM
import time

buzzer = PWM(Pin(6), freq=440, duty=0)

TICK_MS = 10
ONE_BEAT_MS = 400          # 한 박 = 400 ms (빠르게 하려면 숫자를 줄인다)
PEAK = 96                  # 가장 큰 크기 (볼륨 6 쯤)

# 소리 모양 고르기 : "피아노" "오르간" "종" "바이올린" 중 하나로 바꿔 본다
SHAPE = "피아노"
SHAPES = {
    "피아노": (10, 200, 20, 120),
    "오르간": (40, 0, 100, 80),
    "종":     (5, 300, 0, 80),
    "바이올린": (120, 80, 70, 120),
}

# 낮은 음(L), 가운데 음, 높은 음(H) 주파수
L_SOL, L_RA, L_SI = 392, 440, 494
DO, RE, MI, FA, SOL, RA, SI = 523, 587, 659, 698, 784, 880, 988
H_DO, H_RE, H_MI = 1047, 1175, 1319
REST = 0

# [주파수, 박자, 음이름]
# 박자 1 = 한 박, 0.5 = 반 박, 0.25 = 1/4 박, 2 = 두 박
# ▼ 악보를 보고 아기상어 음을 여기에 차례대로 적어 넣는다
#   예) [RE, 0.5, "레"], [MI, 0.5, "미"], [SOL, 0.25, "솔"], ...
song = [
    # 1절
    
    # 2절
    
]

def fit_shape(total, a, d, s, r):
    # 짧은 음(반 박, 1/4 박)이면 어택+디케이+릴리즈 가 음 길이 안에 들어가도록 줄인다
    used = a + d + r
    if used > total:
        a = a * total // used
        d = d * total // used
        r = r * total // used
    return a, d, s, r

def envelope_duty(t, total, peak, a, d, s, r):
    sus = peak * s // 100
    if t < a:
        return peak * t // a
    if t < a + d:
        return peak - (peak - sus) * (t - a) // d
    if t < total - r:
        return sus
    return sus * (total - t) // r

def play_note(freq, total, peak, a, d, s, r):
    buzzer.freq(freq)
    t = 0
    while t < total:
        buzzer.duty(envelope_duty(t, total, peak, a, d, s, r))
        time.sleep_ms(TICK_MS)
        t += TICK_MS
    buzzer.duty(0)

try:
    a, d, s, r = SHAPES[SHAPE]
    print("아기상어 -", SHAPE)
    if not song:
        print("song 목록이 비어 있어요. 악보를 보고 음을 넣어 주세요.")
    for freq, beats, name in song:
        total = int(beats * ONE_BEAT_MS)
        print(name, freq, "Hz", beats, "박")
        if freq == REST:
            buzzer.duty(0)
            time.sleep_ms(total)
        else:
            na, nd, ns, nr = fit_shape(total, a, d, s, r)
            play_note(freq, total, PEAK, na, nd, ns, nr)
        time.sleep_ms(20)   # 같은 음이 이어질 때 끊겨 들리도록 아주 짧게 쉰다
    print("연주 끝")
finally:
    buzzer.duty(0)
    buzzer.deinit()