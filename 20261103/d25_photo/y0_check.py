# y0_check.py : ultralytics 가 설치되었는지 점검한다 (읽지 않고 실행만 하면 된다)
import sys                                   # 파이썬 자신의 정보를 담은 도구 꾸러미

print("파이썬 버전 :", sys.version.split()[0])   # 파이썬 버전 글자에서 맨 앞 낱말(예 : 3.12.10)만 보여 준다

import ultralytics                           # 설치한 ultralytics 를 불러온다 (설치가 안 되었으면 여기서 빨간 오류가 난다)
print("ultralytics 버전 :", ultralytics.__version__)   # ultralytics 의 버전을 보여 준다

import torch                                 # ultralytics 가 계산에 쓰는 torch 를 불러온다
print("torch 버전 :", torch.__version__)      # torch 의 버전을 보여 준다
print("점검 끝 : 세 줄이 모두 나오면 설치가 된 것이다")
