"""BLE 로 받은 바이트를 그대로 쉘에 찍기
폰이 보낸 값이 쉘에 그대로 나온다"""
import bluetooth, ble_simple_peripheral

NAME = "pyD_00"                      # ★ 내 번호로

ble = bluetooth.BLE()
p = ble_simple_peripheral.BLESimplePeripheral(ble, name=NAME)


def on_rx(read):                     # 폰이 값을 써 넣으면 불린다
    print("받음:", read, "길이", len(read))


p.on_write(on_rx)
print("광고 중:", NAME)

try:
    while True:
        pass
except KeyboardInterrupt:
    print("정지")
