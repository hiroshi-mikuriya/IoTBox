from xmlrpc.client import boolean
import RPi.GPIO as GPIO

SERVO_PIN = 13
LED_PIN = 19


class Gpio:
    """
    GPIO操作クラス
    """
    def __init__(self):
        """
        GPIO初期化する
        """
        print('Gpio __init__')
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(SERVO_PIN, GPIO.OUT)
        GPIO.setup(LED_PIN, GPIO.OUT)
        self.servo = GPIO.PWM(SERVO_PIN, 50)
        self.servo.start(0)

    def __del__(self):
        """
        GPIO制御を終了する
        """
        print('Gpio __del__')
        self.servo.stop()
        GPIO.cleanup()

    def led(self, level: bool):
        """
        LEDを点灯・消灯する

        Parameters
        ----------
        level: bool
            True: 点灯する
            False: 消灯する
        """
        GPIO.output(LED_PIN, level)

    def motor(self, n: int):
        """
        モーターを回す

        Parameters
        ----------
        n: int
            0 - 32
        """
        A = 2.5
        B = 12
        R = 32
        duty = (B - A) / R * n + A
        self.servo.ChangeDutyCycle(duty)


if __name__ == '__main__':
    import time
    io = Gpio()
    io.led(True)
    for i in range(32):
        io.motor(i)
        time.sleep(0.1)
    io.led(False)
