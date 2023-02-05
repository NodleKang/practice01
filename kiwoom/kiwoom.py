from PyQt5.QAxContainer import *
from PyQt5.QtCore import *
from config.errCode import *

# PyQt5에 있는 QAxContainer 파일에 있는 모든 클래스 임포트
# QAxContainer에는 마소에서 제공하는 프로세스를 가지고 화면을 구성하는 데 필요한 기능이 포함돼 있음
# 여기서 필요한건 QAxContainer에 속해있는 QAxWidget 임

# QAxWidtet을 상속받아서 그 클래스 안에 있는 내용을 다 가져다 쓰겠다.

# OCX (OLE Custom eXtension)
# 윈도우즈에서 실행할 수 있게 만들어진 특수목적 프로그램, 확장자는 ocx임
# 키움 Open API+는 윈도우즈에 ocx 방식의 컴포넌트 객체로 설치되어 있다
# QAxWidget.setControl은 ocx를 파이썬에서 사용할 수 있게 해줌

# PyQt 관련 개념
# 1. 사용자가 이벤트(예:버튼누르기)를 발생시키는 행위를 "시그널"이라고 하고,
#    "시그널"이 발생했을 때 수행할 함수를 "슬롯"이라고 합니다.
# 2. 이벤트루프에 의해 호출당하는 함수를 콜백(callback) 함수라고 합니다.

# 스레드를 이용하지 않으면 비동기 프로그램을 작성하기 위해서 PyQt를 사용합니다.
# 키움 Open API가 비동기로 처리되기 때문입니다.

# 키움 Open API+
# 키움 Open API+는 윈도우즈에 ocx 방식의 컴포넌트 객체로 설치됩니다.
# 키움 Open API+는 이벤트루프 기반으로 비동기(async) 방식으로 처리됩니다.
# 즉, 함수를 호출한다고 바로 응답이 오는 것은 아닙니다.
# 호출은 순서대로 할 수 있어도 응답은 호출한 순서와 상관없이 언제든 올 수 있습니다.

# PyQt에서 함수를 호출할 때는 dynamicCall() 함수를 사용합니다.
# = 언제 응답이 올지는 모르지만 일단 함수 호출
# 예: self.ocx.dynamicCall("메소드명(파라미터1타입, 파라미터2타입)", 인풋1, 인풋2)

# PyQt에서 응답을 받아 처리하기 위해서 connect() 함수를 사용합니다.
# = 응답이 언제 올지 모르지만 응답으로 특정 이벤트가 오면 미리 정의해둔 함수를 호출하게 할 수 있습니다.
# = 이벤트 루프에 콜백함수 등록
# 예: self.ocx.이벤트명.connect(self.이벤트가 오면 실행될 메소드명)
# 헷갈리니까 이벤트가 오면 호출될 함수 이름은 이벤트와 같은 이름으로 만듭니다.


class Kiwoom:
    """
    키움증권 Open API 처리 클래스
    """

    def __init__(self):
        """
        초기화 메소드
        """
        super().__init__()  # QAxWidget.__init()__ 호출

        # OCX 설정 - 키움 OpenAPI 는 OCX 방식의 컴포넌트 객체로 설치됨
        self.ocx = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")

        # 이벤트에 콜백함수(들)을 등록
        self.set_event_slots()

        # 로그인을 위한 이벤트 루프
        self.login_event_loop = QEventLoop()

        # 키움증권에 로그인
        self.login()
        # 키움증권 로그인 후에 계좌번호 목록가져오기
        self.accno_list = self.get_accno_list()
        # 단일 계좌에 상세 정보 조회
        for accno in self.accno_list:
            self.get_account_detail(accno)

        print(__name__, "started")

    def set_event_slots(self):
        """
        이벤트에 콜백함수(들)을 등록한다.
        PyQt에 의존해서 돌아가는 부분으로 이벤트가 언제 발생할지는 모르지만 
        이벤트가 발생하면 self에 가지고 있는 대응되는 함수를 실행한다.
        """
        # 이벤트 - 로그인 처리
        self.ocx.OnEventConnect.connect(self.OnEventConnect)
        # 이벤트 - 조회와 실시간 데이터 처리
        self.ocx.OnReceiveTrData.connect(self.OnReceiveTrData)

    def login(self):
        """
        키움증권 로그인을 위해 OCX의 CommConnect() 함수를 호출하고 로그인이 될 때까지 기다림
        """
        self.ocx.dynamicCall("CommConnect()")

        self.login_event_loop.exec_()

    def get_accno_list(self):
        """
        키움증권 로그인 후 보유계좌 목록 반환

        GetLoginInfo(tag: str)
            "ACCOUNT_CNT" : 보유계좌 갯수를 반환합니다.
            "ACCLIST" 또는 "ACCNO" : 구분자 ';'로 연결된 보유계좌 목록을 반환합니다.
            "USER_ID" : 사용자 ID를 반환합니다.
            "USER_NAME" : 사용자 이름을 반환합니다.
            "GetServerGubun" : 접속서버 구분을 반환합니다.(1 : 모의투자, 나머지 : 실거래서버)
            "KEY_BSECGB" : 키보드 보안 해지여부를 반환합니다.(0 : 정상, 1 : 해지)
            "FIREW_SECGB" : 방화벽 설정여부를 반환합니다.(0 : 미설정, 1 : 설정, 2 : 해지)
        """
        accno_list = self.ocx.dynamicCall("GetLoginInfo(String)", "ACCLIST")
        return accno_list.split(";")

    def get_account_detail(self, accno: str):
        """
        예수금 상세 현황 조회
        
        CommRqData() : 조회요청함수
            BSTR sRQName,    // 사용자 구분명 (임의로 지정, 한글지원)
            BSTR sTrCode,    // 조회하려는 TR이름
            long nPrevNext,  // 연속조회여부
            BSTR sScreenNo  // 화면번호 (4자리 숫자 임의로 지정)

        키움증권 화면번호(스크린번호)는 request들을 묶는 그룹아이디와 같은 역할이며,
        하나의 화면번호에는 최대 100개 요청까지만 만들 수 있다.
        한 프로그램에서 화면번호 자체는 최대 200개까지 만들 수 있다.

        스크린번호 자체를 날리고 싶을 때
        self.dynamicCall("DisconnectRealData(String)", "스크린번호")
        스크린번호 안애 있는 종목 하나만 날리고 싶을 때
        self.dynamicCall("SetRealRemove(String, String)", "스크린번호", "종목번호")

        Args:
            accno: str 계좌번호

        Returns:

        """
        print("예수금상세현황요청")
        tr_code = "opw00001"  # 조회할 TR 이름
        screen_no = "2000"  # 화면번호

        self.ocx.dynamicCall("SetInputValue(String, String)", "계좌번호", accno)
        self.ocx.dynamicCall("SetInputValue(String, String)", "비밀번호", "0000")
        self.ocx.dynamicCall("SetInputValue(String, String)", "비밀번호입력매체구분", "00")
        self.ocx.dynamicCall("SetInputValue(String, String)", "조회구분", "2")
        self.ocx.dynamicCall(
            "CommRqData(String, String, int, String)",
            "예수금상세현황요청",
            tr_code,
            "0",
            screen_no,
        )

    def OnEventConnect(self, err_code):
        """
        키움증권 로그인 이벤트의 응답 처리

        Args:
            err_code: 연결과정 중에 발생한 에러코드
        """
        # 로그인 함수에서 계속되고 있는 이벤트 루프를 종료함
        self.login_event_loop.exit()

        print(errors(err_code=err_code))
        print("login is done")
        # code = "005930"
        # name = self.GetMasterCodeName(code)
        # print(code, name)

    def GetMasterCodeName(self, code):
        """
        종목명 조회

        Args:
            code: 조회할 종목 코드

        Returns:
            조회된 종목 이름
        """
        name = self.ocx.dynamicCall("GetMasterCodeName(QString)", code)
        return name

    def GetCommData(self, strTrCode, strRecordName, nIndex, strItemName):
        data = self.ocx.dynamicCall(
            "GetCommData(QString, QString, int, QString)",
            strTrCode,
            strRecordName,
            nIndex,
            strItemName,
        )
        return data.strip()

    def OnReceiveTrData(self, sScrNo, sRQName, sTrCode, sRecordName, sPrevNext):
        """
        키움서버에서 응답받은 OnReceiveTrData() 이벤트 처리

        Args:
            sScrNo: 화면번호
            sRQName: 사용자 구분명
            sTrCode: TR이름
            sRecordName: 레코드 이름
            sPrevNext: 연속조회 유무를 판단하는 값 0: 연속(추가조회) 데이터 없음, 2: 연속(추가조회) 데이터 있음

        Returns:

        """

        if sRQName == "예수금상세현황요청":
            deposit = self.GetCommData(sTrCode, sRecordName, 0, "예수금")
            print("예수금 %s" % deposit)
            d2 = self.GetCommData(sTrCode, sRecordName, 0, "출금가능금액")
            print("출금가능금액 %s" % d2)
