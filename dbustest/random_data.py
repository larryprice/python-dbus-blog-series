import dbus.service
import random
import time

import threading
class SlowThread(object):
    def __init__(self, bits, callback):
        self._callback = callback
        self.result = ''

        self.thread = threading.Thread(target=self.work, args=(bits,))
        self.thread.start()
        self.thread_id = str(self.thread.ident)

    def work(self, bits):
        num = ''

        while True:
            num += str(random.randint(0, 1))
            bits -= 1
            time.sleep(1)

            if bits <= 0:
                break

        self._callback(self.thread_id, str(int(num, 2)))

class RandomData(dbus.service.Object):
    def __init__(self, bus_name):
        super().__init__(bus_name, "/com/larry_price/test/RandomData")

        random.seed()

    @dbus.service.method("com.larry_price.test.RandomData",
                         in_signature='i', out_signature='s')
    def quick(self, bits=8):
        return str(random.getrandbits(bits))

    @dbus.service.method("com.larry_price.test.RandomData",
                         in_signature='i', out_signature='s')
    def slow(self, bits=8):
        thread = SlowThread(bits, self.slow_result)
        return thread.thread_id

    @dbus.service.signal("com.larry_price.test.RandomData", signature='ss')
    def slow_result(self, thread_id, result):
        pass
