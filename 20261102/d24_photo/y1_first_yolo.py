from ultralytics import YOLO            # ultralytics 꾸러미에서 YOLO 설계도 하나를 꺼낸다

# ---- 내가 바꾸는 값 ----
PHOTO = "dog.jpg"                       # 같은 폴더에 있는 사진 이름 (따옴표 안의 이름만 바꾼다)

model = YOLO("yolo26n.pt")              # 설계도 YOLO 로 model 을 만든다 : yolo26n.pt 는 이미 배워 둔 결과 파일 (처음 한 번만 내려받는다)
results = model(PHOTO)                  # model 에 사진을 건네면 YOLO 의 답 묶음(results)이 돌아온다
result = results[0]                     # 사진 한 장을 넣었으니 답도 첫째(0번) 하나만 꺼낸다

print("찾은 물체의 개수 :", len(result.boxes))   # boxes 는 찾은 물체들의 목록 : 길이 = 물체 개수
for box in result.boxes:                # 찾은 물체(네모)를 하나씩 꺼내 box 에 넣고 아래 세 줄을 되풀이한다
    name = result.names[int(box.cls[0])]        # box.cls[0] 은 이름의 번호(16.0) → int 로 정수 16 → names 에서 이름 dog 를 찾는다
    confidence = float(box.conf[0])             # box.conf[0] 은 자신감 : float 로 소수(0 ~ 1)로 바꾼다
    print(name, round(confidence, 2))           # 이름과 자신감을 소수 둘째 자리까지 보여 준다

result.save("yolo_result.jpg")          # 네모를 그린 사진을 yolo_result.jpg 파일로 저장한다
print("yolo_result.jpg 로 저장했다")
