from kiwoom.kiwoom import *
import sys

# PyQt5에 있는 QtWidgets 파일에 있는 모든 클래스 임포트 (QApplication 클랙스 포함)
# QApplication 클래스는 프로그램을 앱처럼 실행하거나 홈페이지처럼 실행할 수 있게 그래픽적인 요소룰 제어하는 기능을 포함함, 동시성 처리 함수도 포함돼 있음
from PyQt5.QtWidgets import *


class Main:
    def __init__(self):
        print(__name__, "start")

        # QApplication 인스턴스화, 실행파일 이름이 들어있는 sys.argv를 파라미터로 넘겨줌
        # PyQt5 에서 실행할 파일을 인지하고 동시성 처리를 할 수 있도록 지원함
        self.app = QApplication(sys.argv)
        self.label = QLabel("Hello PyQt")
        self.label.show()

        # 키움 클래스 인스턴스화
        self.kiwoom = Kiwoom()

        # QApplication 클래스에 포함된 exec_() 함수를 실행해서 프로그램이 종료되지 않고, 동시성 처리를 지원하게 함
        # 이벤트 루프 실행
        self.app.exec_()


if __name__ == "__main__":
    Main()
