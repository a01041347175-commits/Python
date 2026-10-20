# D16 블루투스 — 파일 두 개를 보드에 올리고 광고 확인하기

드론키트(01Studio PYDRONE) 보드에서 블루투스 광고를 시작해 폰에 내 보드 이름이 보이게 만듭니다. 펌웨어 `pyDrone.bin` 을 굽고 토니로 연결한 다음, 이 폴더의 라이브러리 두 파일을 토니로 보드에 올립니다.

| 파일 | 한 줄 설명 | 조작 |
|---|---|---|
| `ble_simple_peripheral.py` | 블루투스로 글자를 주고받는 통로를 만든다 (**보드에 올린다**) | 우클릭 → Upload to / |
| `ble_advertising.py` | 폰에 보일 이름 광고 데이터를 만든다 (**보드에 올린다**) | 우클릭 → Upload to / |
| `ble_raw_dump.py` | 확인용 — 광고를 시작하고 폰이 보낸 값을 쉘에 찍는다 | 토니에서 ▶ 실행 (보드에 올리지 않는다) |

**두 라이브러리 파일은 짝이라 모두 올린다.** `ble_simple_peripheral.py` 가 안에서 `ble_advertising.py` 를 다시 불러 쓴다.

## 순서
0. 먼저 펌웨어 `pyDrone.bin` 을 굽고 토니로 연결해 쉘에 `01Studio PYDRONE` 이 보이는지 확인한다 (강의 자료의 앞부분).
1. 토니 위쪽 메뉴 **View → Files** 로 파일 창을 켠다 (이미 켜져 있으면 누르지 않는다).
2. 위쪽 **This computer** 창에서 이 폴더(`d16_블루투스`)를 **더블클릭**해 안으로 들어간다.
3. `ble_advertising.py` 위에서 **마우스 오른쪽 → Upload to /** 를 누른다. 아래 **MicroPython device** 창에 파일이 생기는지 본다.
4. `ble_simple_peripheral.py` 도 같은 방법으로 올린다. MicroPython device 창에 파일 세 개(`ble_advertising.py`, `ble_simple_peripheral.py`, `boot.py`)가 보이면 끝.
5. `ble_raw_dump.py` 를 더블클릭해 열고 초록 ▶ 를 누른다.
6. 쉘에 `MAC: …`, `Starting advertising`, `광고 중: pyD_00` 이 나오면 성공. 확인이 끝나면 빨간 정지 버튼으로 멈춘다 (멈추면 광고도 꺼진다).

## 폰에서 찾기
- **nRF Connect for Mobile** 앱의 **Scanner** 에서 `pyD_00` 을 찾는다. 아이폰은 **설정 앱의 Bluetooth 목록에는 이 보드가 나오지 않는다.**
- 보드가 광고 중(쉘에 `광고 중:`)일 때만 보인다.

## 이름 바꾸기
- `ble_raw_dump.py` 5번째 줄 `NAME = "pyD_00"` 의 숫자를 **내 번호**로 바꾼다 (예: `pyD_07`). 교실에서 이름이 겹치면 내 보드를 못 찾는다.
- 이름은 **영문·숫자 8글자 이내**로 쓴다 (광고 데이터가 31바이트 한도라 길면 광고가 안 될 수 있다).

## 한 줄 정리
| 단계 | 끝났다는 표시 |
|---|---|
| 펌웨어 굽기·토니 연결 | 쉘에 `01Studio PYDRONE` |
| 파일 올리기 | MicroPython device 창에 파일 세 개 |
| 광고 확인 | 쉘에 `광고 중: pyD_00` |
| 폰에서 찾기 | nRF Connect 목록에 내 보드 이름 |
