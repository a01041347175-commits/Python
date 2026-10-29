import numpy as np                  # numpy : 숫자표를 한꺼번에 계산하는 도구
from PIL import Image               # Pillow 의 사진 도구 (사진 열기·바꾸기)

# ---- 내가 바꾸는 값 ----
PHOTO = "dog.jpg"
LIGHT = 0.8                         # 빛의 세기 : 1.0 = 원래 사진, 0.5 = 빛이 절반인 어두운 방, 1.3 = 더 밝은 곳
LINE = 120                          # b1 과 같은 밝기 기준
RED_MIN = 150                       # b3 과 같은 빨간 픽셀 조건 ①
OTHER_MAX = 80                      # b3 과 같은 빨간 픽셀 조건 ②
COUNT_LINE = 20                     # b3 과 같은 개수 기준

# 1) 빛을 바꾼 사진 만들기
numbers = np.array(Image.open(PHOTO).convert("RGB")).astype(int)    # 사진의 숫자표 (빨강·초록·파랑)
numbers = numbers * LIGHT                                           # 모든 픽셀의 숫자에 빛의 세기를 곱한다 (0.8 이면 모두 80 %)
numbers = np.clip(numbers, 0, 255)                                  # 0 ~ 255 밖은 잘라 낸다 (a4 와 같다)
img = Image.fromarray(numbers.astype(np.uint8))                     # 숫자표를 다시 사진으로 되돌린다
img.save("light.jpg")                                               # 빛을 바꾼 사진을 저장한다
print(PHOTO, "빛의 세기", LIGHT, "→ light.jpg 로 저장했다")

# 2) 규칙 1 (b1) : 평균 밝기로 밝은 사진·어두운 사진
average = np.array(img.convert("L")).mean()                         # 모든 픽셀의 평균 밝기
if average > LINE:                                                  # b1 과 같은 규칙 : 기준보다 크면
    print("규칙 1 : 평균 밝기", round(average, 1), "→ 밝은 사진")
else:                                                               # 그렇지 않으면
    print("규칙 1 : 평균 밝기", round(average, 1), "→ 어두운 사진")

# 3) 규칙 2 (b3) : 빨간 픽셀을 세어 빨간 물체가 있는지
small = img.resize((img.width // 10, img.height // 10))             # 픽셀 10 x 10 개를 한 칸으로 줄인다 (b3 과 같다)
count = 0                                                           # 빨간 픽셀 개수 : 0 에서 시작한다
for y in range(small.height):                                       # 세로 : 맨 위 줄부터
    for x in range(small.width):                                    # 가로 : 그 줄의 왼쪽 칸부터
        r, g, b = small.getpixel((x, y))                            # 이 픽셀의 빨강·초록·파랑 숫자
        if r > RED_MIN and g < OTHER_MAX and b < OTHER_MAX:         # b3 과 같은 규칙
            count = count + 1                                       # 개수를 하나 늘린다
if count > COUNT_LINE:                                              # 판단 : 기준 개수보다 많으면
    print("규칙 2 : 빨간 픽셀", count, "개 → 빨간 물체가 있다")
else:                                                               # 그렇지 않으면
    print("규칙 2 : 빨간 픽셀", count, "개 → 빨간 물체가 없다")
