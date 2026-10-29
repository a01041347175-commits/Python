from PIL import Image               # Pillow 의 사진 도구 (사진 열기·바꾸기)

# ---- 내가 바꾸는 값 : 이름을 물어볼 픽셀 ----
PHOTO = "dog.jpg"
X = 150                             # 가로로 몇 번째 픽셀 (0 부터)
Y = 650                             # 세로로 몇 번째 픽셀 (0 부터)

# ---- 예시 : [색 이름, 빨강, 초록, 파랑] — 사진에서 D21 a2 로 잰 숫자 ----
EXAMPLES = [
    ["빨강", 175, 67, 57],          # dog.jpg   (960, 300)  탁자
    ["주황", 234, 124, 13],         # fruit.jpg (1050, 700) 오렌지
    ["노랑", 255, 244, 184],        # fruit.jpg (600, 1600) 바나나
    ["초록", 95, 130, 76],          # zoo.jpg   (100, 100)  나무
    ["파랑", 51, 95, 142],          # drone.jpg (600, 60)   하늘
    ["흰색", 219, 220, 214],        # desk.jpg  (300, 700)  책상
    ["검정", 23, 18, 14],           # fruit.jpg (100, 100)  배경
#    ["갈색", 167, 121, 88],         # fruit.jpg (850, 1120) 키위 : 맨 앞의 # 을 지우면 예시가 하나 늘어난다
]

img = Image.open(PHOTO).convert("RGB")                  # 사진을 연다
r, g, b = img.getpixel((X, Y))                          # 물어볼 픽셀의 빨강·초록·파랑 숫자 (D21 a2 와 같다)
print("물어볼 픽셀", (X, Y), ": 빨강", r, "초록", g, "파랑", b)

best_name = "없음"                  # 지금까지 가장 가까운 예시의 이름 : 처음에는 없다
best_diff = 999                     # 지금까지 본 가장 작은 차이 : 처음에는 아주 큰 값 (D20 r1 의 lo = 4095 와 같은 방법)

for example in EXAMPLES:                                # 예시를 한 줄씩 꺼내 아래 줄들을 반복한다
    diff = abs(r - example[1]) + abs(g - example[2]) + abs(b - example[3])    # 색 숫자 차이 세 개를 더한다 (abs = 빼서 마이너스면 플러스로)
    print("   ", example[0], "예시와의 차이", diff)
    if diff < best_diff:                                # 지금까지 본 것보다 더 가까우면
        best_diff = diff                                # 가장 작은 차이를 바꾸고
        best_name = example[0]                          # 그 예시의 이름을 기억한다

print("가장 가까운 예시 →", best_name, "(차이", best_diff, ")")
