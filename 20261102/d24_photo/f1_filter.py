from PIL import Image
import numpy as np

# ---- 내가 바꾸는 값 ----
PHOTO = "dog.jpg"                       # 같은 폴더에 있는 사진 이름
FILTER = "세로선"                        # "세로선" · "가로선" · "흐리게" 중 하나를 쓴다

# 필터 = 3 x 3 작은 숫자표 (왼쪽 위부터 한 줄씩)
FILTERS = {
    "세로선": [[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]],     # 왼쪽이 어둡고 오른쪽이 밝은 세로 경계를 찾는다
    "가로선": [[-1, -1, -1], [0, 0, 0], [1, 1, 1]],     # 위가 어둡고 아래가 밝은 가로 경계를 찾는다
    "흐리게": [[1, 1, 1], [1, 1, 1], [1, 1, 1]],        # 아홉 칸을 모두 더한다 (아래에서 9 로 나눈다)
}

img = Image.open(PHOTO).convert("L")    # L = 흑백 (칸마다 밝기 숫자 하나)
img.thumbnail((640, 640))               # 너무 큰 사진은 줄인다
table = np.array(img, dtype=float)      # 사진을 숫자표로 바꾼다 (D22 와 같다)
height = table.shape[0]                 # 숫자표의 세로 칸 수
width = table.shape[1]                  # 숫자표의 가로 칸 수

f = np.array(FILTERS[FILTER], dtype=float)   # 고른 필터를 숫자표로 만든다
if FILTER == "흐리게":
    f = f / 9                                # 아홉 칸의 평균이 되게 한다

score = np.zeros((height - 2, width - 2))    # 점수표 (가장자리 한 줄씩 줄어든다)
# 필터를 옮기는 대신, 사진 전체를 한 칸씩 어긋나게 9 번 겹쳐 같은 계산을 한 번에 한다 (결과는 같다)
for i in range(3):                           # 필터의 세로 3 줄
    for j in range(3):                       # 필터의 가로 3 칸
        score = score + f[i][j] * table[i:i + height - 2, j:j + width - 2]   # 겹친 칸끼리 곱해서 더한다

print("필터", FILTER, "를 사진 전체에 밀었다")
print("맨 왼쪽 위 칸의 점수 :", round(score[0][0], 1))

result = np.clip(np.abs(score), 0, 255)      # 점수의 크기를 밝기 0 ~ 255 로 바꾼다
Image.fromarray(result.astype("uint8")).save("filter_result.jpg")
print("filter_result.jpg 로 저장했다 (PyCharm 에서 연다)")
