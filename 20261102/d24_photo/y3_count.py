from ultralytics import YOLO            # ultralytics 도구 상자에서 YOLO 하나만 꺼낸다

# ---- 내가 바꾸는 값 ----
PHOTO = "street.jpg"                    # 같은 폴더에 있는 사진 이름 (따옴표 안에 쓴다)
WANT = "person"                         # 세고 싶은 물체의 이름 (person · car · dog · chair · orange …)

model = YOLO("yolo26n.pt")              # 가장 작은 YOLO 파일을 불러와 model 이라는 이름을 붙인다
results = model(PHOTO)                  # 사진을 보여 준다 (y1·y2 와 같은 두 줄)
result = results[0]                     # 답 묶음의 0번째 = 사진 한 장에 대한 답

count = 0                               # 센 개수 : 처음에는 0 (아직 하나도 세지 않았다)
for box in result.boxes:                # 찾은 네모를 하나씩 꺼낸다
    name = result.names[int(box.cls[0])]        # 이름 번호(정수)를 이름 목록에서 찾아 글자로 바꾼다
    if name == WANT:                    # 이름이 세고 싶은 이름과 같으면
        count = count + 1               # 센 개수에 1 을 더해 다시 count 에 넣는다

print(PHOTO, "에서", WANT, "는", count, "개")     # 사진 이름, 세고 싶은 이름, 센 개수를 한 줄로 쓴다
result.save("yolo_count.jpg")           # 네모를 그린 사진을 파일로 저장한다
