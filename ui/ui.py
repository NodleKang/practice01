from kiwoom.kiwoom import *

import sys
from PyQt5.QtWidgets import *


class UIClass:
    def __init__(self):
        print("UIClass init")

        # sys.argv = 아규먼트가 리스트 형식으로 담겨있음, 리스트의 첫번째 엘리먼트에 이 프로그램 실행경로가 담김
        self.app = QApplication(sys.argv)  # UI 초기화, 어떤 파일을 이용해서 app을 띄울지 지정함

        Kiwoom()

        self.app.exec_()  # 이벤트루프 실행,
        # PyQt5에서는 이벤트루프를 실행하면 명시적으로 종료하지 않으면 프로그램이 종료되지 않음,
        # 프로그램이 계속 실행되게 만드는 효과가 있음


if __name__ == "__main__":
    UIClass()
