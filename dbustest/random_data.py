import dbus.service
import random

class RandomData(dbus.service.Object):
    def __init__(self, bus_name):
        super().__init__(bus_name, "/com/larry_price/test/RandomData")
        random.seed()

    @dbus.service.method("com.larry_price.test.RandomData",
                         in_signature='i', out_signature='s')
    def quick(self, bits=8):
        return str(random.getrandbits(bits))
