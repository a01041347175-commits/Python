from PIL import Image

# ---- 내가 바꾸는 값 ----
PHOTO = "cat.jpg"
X = 300                          # 가로로 몇 번째 픽셀 (0 부터)
Y = 200                          # 세로로 몇 번째 픽셀 (0 부터)

img = Image.open(PHOTO)          # 사진을 열어 img 라는 이름표를 붙인다
r, g, b = img.getpixel((X, Y))   # img.getpixel : (X, Y) 자리 픽셀의 숫자 3개를 r, g, b 에 하나씩 담는다
print("픽셀", (X, Y), "의 색 : 빨강", r, "초록", g, "파랑", b)

gray = img.convert("L")          # img.convert("L") : 흑백 사진으로 바꾼다 (L = 밝기). 픽셀마다 숫자 하나, 0 ~ 255
print("같은 픽셀의 흑백 밝기 :", gray.getpixel((X, Y)))   # 흑백 사진에서 같은 자리의 숫자 하나

print("이 픽셀 주변 5 x 5 칸의 흑백 밝기 :")
for dy in range(5):              # 바깥 반복 : dy 가 0, 1, 2, 3, 4 를 차례로 받는다 (아래로 내려가는 칸 수, 5줄)
    row = []                     # 이번 줄의 숫자를 담을 빈 상자(빈 리스트)를 줄마다 새로 만든다
    for dx in range(5):          # 안쪽 반복 : dx 가 0, 1, 2, 3, 4 를 차례로 받는다 (오른쪽으로 가는 칸 수, 줄마다 5번)
        row.append(gray.getpixel((X + dx, Y + dy)))   # row.append(값) : 상자 row 의 맨 뒤에 값을 하나 넣는다
    print(row)                   # 안쪽 반복이 끝나 상자에 5개가 차면 한 줄을 찍는다
