import serial
import time
import threading

EMPTY = b''


class Uart:
    """
    UART通信クラス
    """
    def __init__(self, port: str, baudrate: int):
        """
        UARTデバイスをオープンする

        Parameters
        ----------
        port : str
            UARTデバイスパス
        baudrate : int
            ボーレート
        """
        print('Uart __init__')
        self.uart = serial.Serial(port=port, baudrate=baudrate, timeout=0.1)
        self.__makeThread()

    def __del__(self):
        """
        UARTデバイスをクローズする
        """
        print('Uart __del__')
        self.__stopThread()
        self.uart.close()

    def __makeThread(self):
        """
        スレッドを作成・開始する
        """
        self.enableThread = True
        self.thread = threading.Thread(target=self.__recvLoop)
        self.lock = threading.Lock()
        self.recvedData = EMPTY
        self.thread.start()

    def __stopThread(self):
        """
        スレッドを停止する
        """
        self.enableThread = False
        self.thread.join()

    def __recvLoop(self):
        """
        スレッド内部処理の実装
        """
        while self.enableThread:
            bin = self.uart.read_all()
            if bin == EMPTY:
                continue
            # １回の通信では読み切らないことがあるので、受信なしになるまでリトライする
            while True:
                time.sleep(0.001)
                res = self.uart.read_all()
                if res == EMPTY:
                    break
                bin += res
            self.lock.acquire()
            self.recvedData = bin
            self.lock.release()

    def waitForRecv(self) -> bytes:
        """
        コマンド受信完了するまで待機する

        Returns
        -------
        command: bytes
            受信したコマンド
        """
        self.lock.acquire()
        self.recvedData = EMPTY
        self.lock.release()
        while self.enableThread:
            time.sleep(0.1)
            res = EMPTY
            self.lock.acquire()
            res = self.recvedData
            self.lock.release()
            if res != EMPTY:
                return res
        return EMPTY


if __name__ == '__main__':
    uart = Uart('/dev/ttyS0', 9600)
    s = uart.waitForRecv()
    print("read data:", s.decode('utf8').replace('\r', ''))
