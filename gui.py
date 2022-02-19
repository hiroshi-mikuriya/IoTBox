import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from redis_adapter import RedisAdapter


class MainWindow(QMainWindow):
    """
    メインウィンドウクラス
    """
    def __init__(self):
        """
        コンストラクタ
        """
        super().__init__()
        self.redis = RedisAdapter()
        self.__initUI()
        self.__startTimer()

    def __initUI(self):
        """
        画面初期化する
        """
        self.setStyleSheet('background-color: black;')
        self.label = QLabel(self)
        self.label.setStyleSheet('color: white;'
                                 'min-width: 800px;'
                                 'min-height: 200px;'
                                 'font-size: 50px;'
                                 'padding-top: 40px;'
                                 'padding-left: 50px;')

    def __startTimer(self):
        """
        タイマーを開始する
        """
        self.timer = QTimer()
        self.timer.timeout.connect(self.__on_timeout)
        self.timer.start(500)

    def __on_timeout(self):
        """
        タイマーイベント発生時に呼び出される関数
        """
        main = self.redis.getText().decode('utf-8')
        self.label.setText(main)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    windows = MainWindow()
    windows.showFullScreen()
    app.exec_()
    sys.exit(0)
