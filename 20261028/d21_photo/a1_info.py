from PIL import Image

# ---- 내가 바꾸는 값 ----
PHOTO = "cat.jpg"                # 같은 폴더에 있는 사진 이름

img = Image.open(PHOTO)          # Image.open : 사진 파일을 열어서 img 라는 이름표를 붙인다
print("가로", img.width, "픽셀")   # img.width : 사진의 가로 픽셀 수
print("세로", img.height, "픽셀")  # img.height : 사진의 세로 픽셀 수
print("픽셀의 개수", img.width * img.height, "개")   # 가로 x 세로 = 사진 전체의 픽셀 수
print("색 방식", img.mode)        # img.mode : RGB = 픽셀마다 빨강·초록·파랑 숫자 3개
