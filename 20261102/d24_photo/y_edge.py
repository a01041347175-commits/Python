import cv2

# ---- 내가 바꾸는 값 ----
PHOTO = "dog.jpg"                       # 같은 폴더에 있는 사진 이름
LOW = 100                               # 윤곽선 후보로 받아 주는 가장 약한 기준 (작을수록 윤곽이 많아진다)
HIGH = 200                              # 확실한 윤곽선이라고 보는 기준 (LOW 보다 크게 쓴다)

img = cv2.imread(PHOTO)                 # 사진 파일을 숫자표로 읽는다 (D22 에서 본 숫자표와 같다)
height = img.shape[0]                   # 숫자표의 세로 칸 수
width = img.shape[1]                    # 숫자표의 가로 칸 수

edges = cv2.Canny(img, LOW, HIGH)       # 윤곽선만 남긴 흑백 숫자표를 만든다 (윤곽 = 255, 나머지 = 0)

count = cv2.countNonZero(edges)         # 0 이 아닌 칸, 즉 윤곽선 칸의 개수를 센다
print(PHOTO, "기준", LOW, HIGH, "→ 윤곽 칸", count, "개 /", height * width, "칸 중")

cv2.imwrite("edge_result.jpg", edges)   # 윤곽선 사진을 파일로 저장한다 (PyCharm 에서 연다)
print("edge_result.jpg 로 저장했다")
