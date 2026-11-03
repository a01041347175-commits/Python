from ultralytics import YOLO            # ultralytics 도구 상자에서 YOLO 하나만 꺼낸다

# ---- 내가 바꾸는 값 ----
PHOTO = "street.jpg"                    # 같은 폴더에 있는 사진 이름 (따옴표 안에 쓴다)
CONF = 0.25                             # 자신감 기준 : 자신감이 이 숫자보다 낮은 네모는 버린다 (0 ~ 1 사이, 0.25 는 YOLO 의 처음 기준)

model = YOLO("yolo26n.pt")              # 가장 작은 YOLO 파일을 불러와 model 이라는 이름을 붙인다
results = model(PHOTO, conf=CONF)       # 사진을 보여 준다 : 왼쪽 conf 는 YOLO 가 정한 이름, 오른쪽 CONF 는 내가 위에서 정한 숫자
result = results[0]                     # 답 묶음의 0번째 = 사진 한 장에 대한 답

print("자신감 기준", CONF, "→ 찾은 물체의 개수 :", len(result.boxes))     # len : 기준을 넘어 남은 네모의 수
for box in result.boxes:                # 남은 네모를 하나씩 꺼낸다
    name = result.names[int(box.cls[0])]        # 이름 번호(정수)를 이름 목록에서 찾아 글자로 바꾼다
    confidence = float(box.conf[0])             # 이 네모의 자신감 (0 ~ 1 사이 소수)
    print("   ", name, round(confidence, 2))    # 이름과 자신감을 소수 둘째 자리까지 쓴다

result.save("yolo_conf.jpg")            # 네모를 그린 사진을 파일로 저장한다
print("yolo_conf.jpg 로 저장했다")
