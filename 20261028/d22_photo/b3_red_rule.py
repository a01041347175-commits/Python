from PIL import Image               # Pillow 의 사진 도구 (사진 열기·바꾸기)

# ---- 내가 바꾸는 값 ----
PHOTO = "dog.jpg"
RED_MIN = 150                       # 빨간 픽셀의 조건 ① : 빨강 숫자가 이보다 커야 한다
OTHER_MAX = 80                      # 빨간 픽셀의 조건 ② : 초록·파랑 숫자는 이보다 작아야 한다
COUNT_LINE = 20                     # 빨간 픽셀이 이 개수보다 많으면 '빨간 물체가 있다'

img = Image.open(PHOTO).convert("RGB")                          # 사진을 연다
small = img.resize((img.width // 10, img.height // 10))         # D21 a5 처럼 픽셀 10 x 10 개를 한 칸으로 줄인다 (세는 시간을 줄인다)
mark = small.copy()                                             # copy() : 찾은 픽셀을 칠해 볼 복사본을 만든다
count = 0                                                       # 빨간 픽셀 개수 : 0 에서 시작한다

for y in range(small.height):                                   # 세로 : 맨 위 줄(0)부터 맨 아래 줄까지
    for x in range(small.width):                                # 가로 : 그 줄의 왼쪽 칸(0)부터 오른쪽 칸까지
        r, g, b = small.getpixel((x, y))                        # 이 픽셀의 빨강·초록·파랑 숫자 (D21 a2 와 같다)
        if r > RED_MIN and g < OTHER_MAX and b < OTHER_MAX:     # 규칙 : 빨강은 크고, 초록도 작고, 파랑도 작으면
            count = count + 1                                   # 개수를 하나 늘린다
            mark.putpixel((x, y), (0, 255, 0))                  # putpixel() : 그 픽셀을 연두색으로 칠한다

print(PHOTO, "줄인 크기", small.width, "x", small.height, "= 픽셀", small.width * small.height, "개")
print("규칙에 맞는 빨간 픽셀", count, "개")
if count > COUNT_LINE:                                          # 판단 : 빨간 픽셀이 기준보다 많으면
    print("→ 빨간 물체가 있다")
else:                                                           # 그렇지 않으면
    print("→ 빨간 물체가 없다")

big = mark.resize(img.size, Image.NEAREST)                      # D21 a5 처럼 원래 크기로 다시 키운다 (칸이 네모로 보인다)
big.save("red_found.jpg")                                       # 같은 폴더에 저장한다
print("red_found.jpg 로 저장했다 (연두색 = 규칙이 빨강이라고 고른 픽셀)")
big.show()                                                      # 화면에 띄운다
