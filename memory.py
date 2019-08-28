from time import sleep
class memory:
    blocks = []
    adress = 0
    ready = False
    def __init__(self, delay, bus):
        self.delayTime = delay
        self.bus = bus

    def read(self, address):
        self.ready = False
        sleep(self.delayTime)
        self.bus.update()
        self.ready = True