import dbus.service
import random
import time

import threading
class SlowThread(object):
    def __init__(self, bits):
        self.finished = threading.Event()
        self.result = ''

        self.thread = threading.Thread(target=self.work, args=(bits,))
        self.thread.start()
        self.thread_id = str(self.thread.ident)

    @property
    def done(self):
        return self.finished.is_set()

    def work(self, bits):
        num = str(random.randint(0, 1))
        while bits > 1:
            num += str(random.randint(0, 1))
            bits -= 1
            time.sleep(1)

        self.result = str(int(num, 2))
        self.finished.set()

class RandomData(dbus.service.Object):
    def __init__(self, bus_name):
        super().__init__(bus_name, "/com/larry_price/test/RandomData")

        random.seed()
        self.threads = []

    @dbus.service.method("com.larry_price.test.RandomData",
                         in_signature='i', out_signature='s')
    def quick(self, bits=8):
        return str(random.getrandbits(bits))

    @dbus.service.method("com.larry_price.test.RandomData",
                         in_signature='i', out_signature='s')
    def slow(self, bits=8):
        thread = SlowThread(bits)
        self.threads.append(thread)
        return thread.thread_id

    @dbus.service.method("com.larry_price.test.RandomData",
                         in_signature='s', out_signature='s')
    def slow_result(self, thread_id):
        thread = [t for t in self.threads if t.thread_id == thread_id]
        if not thread:
            return 'No thread matching id %s' % thread_id

        thread = thread[-1]
        if thread.done:
            result = thread.result
            self.threads.remove(thread)
            return result

        return ''
