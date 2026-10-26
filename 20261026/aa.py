
from machine import Pin, PWM
from time import sleep

# 부저 연결 GPIO
buzzer = PWM(Pin(6), freq=1000, duty_u16=0)

# 음계별 주파수 (Hz)
notes = {
    "C4": 262,  # 도
    "D4": 294,  # 레
    "E4": 330,  # 미
    "F4": 349,  # 파
    "G4": 392,  # 솔
    "A4": 440,  # 라
    "B4": 494,  # 시
    "C5": 523,  # 높은 도
    "D5": 587,  # 높은 레
    "E5": 659,  # 높은 미
    "R": 0      # 쉼표
}

# 템포 72 BPM
beat = 60 / 72

# (음계, 박자)
melody = [
    # 1~4마디
    ("C4", 1), ("E4", 1),
    ("G4", 1), ("E4", 1),

    ("G4", 1), ("B4", 0.5),
    ("D5", 0.5), ("B4", 2),

    ("A4", 1), ("C5", 1),
    ("E5", 1), ("C5", 1),

    ("F4", 1), ("A4", 1),
    ("C5", 1), ("A4", 1),

    # 5~8마디
    ("E4", 1), ("G4", 1),
    ("C5", 1), ("G4", 1),

    ("D4", 1), ("G4", 1),
    ("B4", 1), ("A4", 1),

    ("F4", 1), ("A4", 1),
    ("G4", 1), ("F4", 1),

    ("E4", 1), ("D4", 1),
    ("C4", 2),

    # 9~12마디
    ("C4", 1), ("E4", 1),
    ("G4", 1), ("C5", 1),

    ("B4", 1), ("G4", 1),
    ("D5", 1), ("B4", 1),

    ("A4", 1), ("C5", 1),
    ("B4", 1), ("A4", 1),

    ("G4", 1), ("F4", 1),
    ("E4", 1), ("D4", 1),

    # 13~16마디
    ("E4", 1), ("G4", 1),
    ("C5", 1), ("B4", 1),

    ("A4", 1), ("G4", 1),
    ("E4", 1), ("D4", 1),

    ("F4", 1), ("A4", 1),
    ("G4", 1), ("E4", 1),

    ("D4", 1), ("C4", 3)
]

# 부저 연주 함수
def play_note(note, duration):
    freq = notes[note]

    if freq == 0:
        buzzer.duty_u16(0)
        sleep(duration)
    else:
        buzzer.freq(freq)
        buzzer.duty_u16(500)
        sleep(max(0, duration - 0.05))
        buzzer.duty_u16(0)
        sleep(min(0.05, duration))

# 반복 재생
try:
    while True:
        for note, beats in melody:
            play_note(note, beat * beats)

        sleep(2)

except KeyboardInterrupt:
    buzzer.duty_u16(0)
    buzzer.deinit()
