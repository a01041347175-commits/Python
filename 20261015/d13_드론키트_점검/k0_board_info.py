# k0_board_info.py — 보드가 누구인지, 메모리와 파일은 어떤지 쉘에 찍는다
import os
import gc
import machine

print("보드 정보 :", os.uname()[4])
print("MicroPython :", os.uname()[3][:20])
print("CPU 속도 :", machine.freq() // 1000000, "MHz")
print("남은 메모리 :", gc.mem_free(), "바이트")
print("보드 안 파일 :", os.listdir())
