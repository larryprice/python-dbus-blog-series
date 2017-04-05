import dbus.service
import random
import time

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
        maximum = 2**bits
        num = random.randint(0, min(512, maximum)-1)
        while num.bit_length() < bits:
            num += random.randint(0, min(512, maximum-int(num))-1)
            time.sleep(1)

        return str(num)
