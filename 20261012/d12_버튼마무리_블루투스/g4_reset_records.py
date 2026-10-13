# 저장된 기록을 모두 지운다 (처음부터 다시 겨루고 싶을 때)
import os

for name in ("best.txt", "cog_log.txt"):
    try:
        os.remove(name)
        print(name, "지웠습니다")
    except OSError:
        print(name, "원래 없었습니다")
