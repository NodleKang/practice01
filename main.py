import sys
from PyQt5.QtWidgets import *

from kiwoom.kiwoom import *

# from pykiwoom.kiwoom import *


class MyWindow(QMainWindow):
    """
    QMainWindow를 상속받아 윈도우 기반의 클래스를 만들어서 사용.
    PyQt에서 모든 위젯의 가장 기초가 되는 위젯을 "윈도우"라고 부름.
    """

    def __init__(self):
        """
        초기화 함수 - 클래스를 이용한 객체(인스턴스) 생성시 자동 호출
        """
        super().__init__()

        self.setWindowTitle("My HTS v1.0")
        self.setGeometry(300, 300, 500, 500)

        btn = QPushButton(text="매수", parent=self)
        btn.move(10, 10)

        # 키움증권용 객체(인스턴스) 생성
        self.kiwoom = Kiwoom()
        # self.kiwoom.CommConnect(block=True)  # block=True 로그인이 완료될 때까지 다음 줄 실행 안 함


# QtWidget 모듈에 정의돼 있는 QApplication 클래스가 있고,
# QApplication 클래스의 객체(인스턴스)를 생성할 때는
# 현재 소스코드 파일에 대한 경로를 담고 있는 파이썬 리스트를 생성자에 전달해야 함
# PuQt5를 이용한 모든 프로그램은 반드시 QApplication객체를 생성해야 함
app = QApplication(sys.argv)
print(sys.argv)

# 이벤트루프 시작 전에 윈도우를 보여줘야 함
window = MyWindow()
window.show()

# 생성된 QApplication 객체의 exec_() 함수를 호출해서 이벤트 루프 시작
# 이벤트 루프가 시작되면 GUI 프로그램은 사용자가 닫기 버튼을 누를 때까지 종료하지 않고 계속 실행됨
app.exec_()  # 이벤트루프 시작

# 이벤트 루프? 반복문 안에서 사용자로 부터의 입력 이벤트 처리
# 이벤트 루프 구조
# while True:
#     이벤트가 있으면 처리
#     if 종료이벤트발생:
#         break
