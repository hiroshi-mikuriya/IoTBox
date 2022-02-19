from uart import Uart
from gpio import Gpio
import time
from redis_adapter import RedisAdapter

UART_PATH = '/dev/ttyS0'
BAUDRATE = 9600


def waitForRecv(uart: Uart):
    """
    UARTコマンド受信まで待機する

    Parameters
    ----------
    uart: Uart
        UART通信オブジェクト
    
    Returns
    -------
    command: str
        受信コマンド文字列
    """
    while True:
        try:
            return uart.waitForRecv().decode('utf8').replace('\r', '')
        except UnicodeDecodeError as e:
            print(type(e))
            print(e)


def run(io: Gpio, uart: Uart):
    """
    メイン処理を実行する

    Parameters
    ----------
    io: Gpio
        GPOI操作オブジェクト
    uart: Uart
        UART通信オブジェクト
    """
    CLOSE = 0  # ゴミ箱が閉じているときのサーボ値
    OPEN = 16  # ゴミ箱が開いているときのサーボ値
    io.motor(CLOSE)
    io.led(False)
    per = 0  # リサイクル達成率のダミーデータ
    db = RedisAdapter()
    while True:
        db.set('バーコードを読み取ります。')
        text = waitForRecv(uart)
        db.set(text)
        io.led(True)
        time.sleep(1.0)
        db.set('読み取りました。')
        io.led(False)
        io.motor(OPEN)
        for i in range(5, 0, -1):
            db.set('投入してください。 {0}sec'.format(i))
            time.sleep(1.0)
        db.set('リサイクル達成率 {0}%'.format(per))
        for i in range(OPEN, CLOSE, -1):
            io.motor(i)
            time.sleep(0.05)
        io.motor(CLOSE)
        time.sleep(1.0)
        # ダミーのリサイクル達成率を更新する
        per += 10
        if 100 < per:
            per = 0


if __name__ == '__main__':
    try:
        io = Gpio()
        uart = Uart(UART_PATH, BAUDRATE)
        run(io, uart)
    except KeyboardInterrupt:
        pass
