import numpy as np                  # numpy : 숫자표를 한꺼번에 계산하는 도구
from PIL import Image               # Pillow 의 사진 도구 (사진 열기·바꾸기)

# ---- 내가 바꾸는 값 ----
PHOTOS = ["street.jpg", "cat.jpg", "dog.jpg", "desk.jpg", "fruit.jpg", "moto.jpg", "drone.jpg", "zoo.jpg"]

for name in PHOTOS:                                     # 사진 이름을 하나씩 꺼내 아래 줄들을 반복한다
    img = Image.open(name).convert("RGB")               # 사진을 연다 (RGB = 픽셀마다 빨강·초록·파랑 숫자 3개)
    red_part, green_part, blue_part = img.split()       # split() : 사진을 빨강만·초록만·파랑만 담은 숫자표 세 장으로 나눈다
    red = np.array(red_part).mean()                     # 모든 픽셀의 빨강 숫자 평균
    green = np.array(green_part).mean()                 # 모든 픽셀의 초록 숫자 평균
    blue = np.array(blue_part).mean()                   # 모든 픽셀의 파랑 숫자 평균
    print(name, "평균 색 : 빨강", round(red), "초록", round(green), "파랑", round(blue))
    if red > green and red > blue:                      # 규칙 1 : 빨강이 초록보다도 크고 파랑보다도 크면
        print("    → 빨강이 가장 많은 사진")
    elif green > red and green > blue:                  # 규칙 2 : (규칙 1 이 아니고) 초록이 가장 크면
        print("    → 초록이 가장 많은 사진")
    else:                                               # 둘 다 아니면 (남은 것은 파랑)
        print("    → 파랑이 가장 많은 사진")
