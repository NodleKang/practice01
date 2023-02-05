from pykiwoom.kiwoom import *

kiwoom = Kiwoom()
kiwoom.CommConnect(block=True)

df = kiwoom.block_request("opt10001", 종목코드="005930", output="주식기본정보", next=0)
df = kiwoom.block_request(
    "opw00001",
    계좌번호="8039479111",  # 7011626131
    비밀번호="0000",
    비밀번호입력매체구분="00",
    조회구분="2",
    output="예수금청세현황요청",
    next=0,
)
print(df)
