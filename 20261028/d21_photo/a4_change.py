import numpy as np
from PIL import Image

# ---- 내가 바꾸는 값 ----
PHOTO = "cat.jpg"
AMOUNT = 60                      # 모든 픽셀의 밝기에 더할 숫자 (마이너스면 어두워진다)

gray = np.array(Image.open(PHOTO).convert("L")).astype(int)    # 흑백 숫자표. .astype(int) : 255 를 넘는 숫자도 담기도록 정수 형식으로 바꾼다
changed = np.clip(gray + AMOUNT, 0, 255)                        # gray + AMOUNT : 모든 칸에 한꺼번에 더한다. np.clip(…, 0, 255) : 0 보다 작으면 0, 255 보다 크면 255 로 자른다
result = Image.fromarray(changed.astype(np.uint8))              # Image.fromarray : 숫자표를 사진으로 되돌린다. .astype(np.uint8) : 0 ~ 255 만 담는 사진용 형식
result.save("changed.jpg")                                      # result.save : 사진 파일로 저장한다
print("changed.jpg 로 저장했다 : 모든 픽셀에", AMOUNT, "을 더했다")
print("평균 밝기", round(gray.mean(), 1), "→", round(changed.mean(), 1))   # round(숫자, 1) : 소수 한 자리로 줄인다
result.show()                                                   # result.show : 사진을 화면 창에 띄운다
