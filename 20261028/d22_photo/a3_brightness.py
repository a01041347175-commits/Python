import numpy as np                                      # numpy 를 가져와 np 라는 짧은 이름으로 부른다
from PIL import Image                                   # Pillow 의 Image 를 가져온다

# ---- 내가 바꾸는 값 : 비교할 사진들 ----
PHOTOS = ["street.jpg", "cat.jpg", "dog.jpg", "desk.jpg", "fruit.jpg", "moto.jpg", "drone.jpg", "zoo.jpg"]   # [ ] 안에 이름 8개 : 리스트(목록)

for name in PHOTOS:                                     # 목록에서 이름을 하나씩 꺼내 name 이라 부르며, 아래 들여쓴 줄을 8번 반복한다
    gray = np.array(Image.open(name).convert("L"))      # 안쪽부터 읽는다 : ① Image.open(name) 사진 열기 → ② .convert("L") 흑백으로 → ③ np.array(...) 숫자표로
    average = gray.mean()                               # gray.mean() : 숫자표 전체의 평균 밝기 (0 ~ 255)
    print(f"{name:12s} 평균 밝기 {average:6.1f}  가장 어두운 픽셀 {gray.min():3d}  가장 밝은 픽셀 {gray.max():3d}")   # f"…{값}…" : { } 자리에 값을 끼워 찍는다. gray.min() 최솟값, gray.max() 최댓값
