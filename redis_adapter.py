import redis

MAIN_TEXT_KEY = 'main-text'


class RedisAdapter:
    """
    画面に表示する文字列をRedisServerに設定するクラス
    """
    def __init__(self):
        """
        コンストラクタ
        """
        self.db = redis.StrictRedis(host='localhost', port=6379, db=0)

    def set(self, text: str):
        """
        文字列をRedisServerに設定する

        Parameters
        ----------
        text: str
            画面に表示する文字列
        """
        print(text)
        self.db.set(MAIN_TEXT_KEY, text)

    def __get(self, key: str):
        """
        キーを指定してRedisServerから文字列を取得する

        Parameters
        ----------
        key: str
            キー

        Returns
        -------
        text: str
            文字列
        """
        return self.db.get(key)

    def getText(self):
        """
        RedisServerからメイン文字列を取得する

        Returns
        -------
        text: str
            メイン文字列
        """
        return self.__get(MAIN_TEXT_KEY)


if __name__ == '__main__':
    import time
    r = RedisAdapter()
    r.set('バーコードを読み取ります。')
    time.sleep(2)
    r.set('読み取りました。')
    time.sleep(1)
    r.set('1234567890')
    time.sleep(1)
    for i in range(5, 0, -1):
        r.set('投入してください。 {0}sec'.format(i))
        time.sleep(1)
    r.set('リサイクル達成率 {0}%'.format(100))
    time.sleep(1)
