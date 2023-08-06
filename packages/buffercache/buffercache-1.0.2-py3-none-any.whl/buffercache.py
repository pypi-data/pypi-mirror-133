__version__ = '1.0.2'
import time


class BufferCache():
    def __init__(self, timeout=None):
        self._timeout = timeout
        self._timestamp = None
        self._data = None
        self._getter = None

    @staticmethod
    def _timestamp_ms():
        # timeout检测精度, 毫秒
        return int(round(time.time() * 1000))

    def _wait(self):
        # 没有设置timeout则允许更新
        if self._timeout is None:
            return True
        # 设置的timeout小于零则允许更新
        if self._timeout <= 0:
            return True

        timestamp = self._timestamp_ms()

        # 第一次获取数据允许更新
        if self._timestamp is None:
            self._timestamp = timestamp
            return True

        # 时间间隔大于timeout则允许更新
        if timestamp - self._timestamp > self._timeout:
            self._timestamp = timestamp
            return True

        # 没有达到timeout时间, 不允许更新
        return False

    @property
    def data(self):
        return self._data

    @property
    def getter(self):
        return self._getter

    def immediate(self, *args, **kwargs):
        if self._getter:
            self.set(self._getter(*args, **kwargs))
        return self

    def update(self, *args, **kwargs):
        if self._getter and self._wait():
            self.set(self._getter(*args, **kwargs))
        return self

    def get(self):
        return self._data

    def get_getter(self):
        return self._getter

    def set(self, data):
        self._data = data
        return self

    def set_getter(self, getter):
        self._getter = getter
        return self

    def __str__(self):
        return "{}".format(self._data)

    def __repr__(self):
        return "buffercache.BufferCache(data={}, getter={}, timeout={}, timestamp={})".format(
            self._data,
            self._getter.__name__ if self._getter else None,
            self._timeout,
            self._timestamp,)
