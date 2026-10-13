import network, socket, time
from camera import Camera, FrameSize, PixelFormat

SSID = "여기에_와이파이_이름"                   # ★ 화면에 안내된 와이파이 이름으로 바꾼다
PASSWORD = "여기에_비밀번호"                    # ★ 화면에 안내된 비밀번호로 바꾼다

SIZE = FrameSize.QVGA                           # 화면 크기: QQVGA(작다) < QVGA < VGA(크다)
QUALITY = 50                                    # 화질 (높을수록 선명하고 느리다)

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)
while not wlan.isconnected():
    time.sleep_ms(300)
ip = wlan.ifconfig()[0]

cam = Camera(pixel_format=PixelFormat.JPEG, frame_size=SIZE)
cam.quality = QUALITY
print("브라우저에 이 주소를 입력하세요 → http://" + ip)

PAGE = (b"HTTP/1.0 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n"
        b"<html><body style='font-size:32px;text-align:center'>"
        b"<h1>ESP32-CAM 실시간 영상</h1><img src='/stream'>"
        b"</body></html>")

server = socket.socket()
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(("0.0.0.0", 80))
server.listen(2)

try:
    while True:
        client, addr = server.accept()
        request = client.recv(512).decode()
        path = request.split(" ")[1] if " " in request else "/"
        print("요청:", addr[0], path)
        if path == "/stream":
            client.send(b"HTTP/1.0 200 OK\r\n"
                        b"Content-Type: multipart/x-mixed-replace; boundary=frame\r\n\r\n")
            try:
                while True:                     # 사진을 쉬지 않고 이어서 보낸다 = 영상
                    photo = cam.capture()
                    client.send(b"--frame\r\nContent-Type: image/jpeg\r\n"
                                b"Content-Length: %d\r\n\r\n" % len(photo))
                    client.send(photo)
                    client.send(b"\r\n")
            except OSError:
                print("브라우저가 닫혔습니다")   # 탭을 닫으면 여기로 온다
        else:
            client.send(PAGE)
        client.close()
except KeyboardInterrupt:
    pass
finally:
    server.close()
    cam.deinit()
    print("정지")

# ⭐ 도전: SIZE 를 QQVGA 로, QUALITY 를 20 으로 바꿔 영상이 더 부드러워지는지 보자.
