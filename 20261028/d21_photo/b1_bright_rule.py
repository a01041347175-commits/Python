import numpy as np                  # numpy : 숫자표를 한꺼번에 계산하는 도구
from PIL import Image               # Pillow 의 사진 도구 (사진 열기·바꾸기)

# ---- 내가 바꾸는 값 ----
PHOTOS = ["street.jpg", "cat.jpg", "dog.jpg", "desk.jpg", "fruit.jpg", "moto.jpg", "drone.jpg", "zoo.jpg"]
LINE = 120                          # 밝기 기준 : 평균 밝기가 이 숫자보다 크면 '밝은 사진' (0 ~ 255 사이에서 고른다)

for name in PHOTOS:                                     # 사진 이름을 하나씩 꺼내 아래 4줄을 반복한다
    gray = np.array(Image.open(name).convert("L"))     # 사진을 흑백 숫자표로 바꾼다 (D21 a3 과 같은 줄)
    average = gray.mean()                               # 모든 픽셀의 평균 밝기 (0 ~ 255)
    if average > LINE:                                  # 규칙 : 평균이 기준보다 크면
        print(name, "평균 밝기", round(average, 1), "→ 밝은 사진")
    else:                                               # 그렇지 않으면 (기준과 같거나 작으면)
        print(name, "평균 밝기", round(average, 1), "→ 어두운 사진")
