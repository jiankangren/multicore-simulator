from time import sleep

class memory:
    data = {
        0x0:'mem',#
        0x1:'mem',#
        0x2:'mem',#
        0x3:'mem',#
        0x4:'mem',#
        0x5:'mem',#
        0x6:'mem',#
        0x7:'mem',# 
        0x8:'mem',#
        0x9:'mem',#
        0xA:'mem',#
        0xB:'mem',#
        0xC:'mem',#
        0xD:'mem',#
        0xE:'mem',#
        0xF:'mem' #        
        }
    size = 16

    def __init__(self, update):
        self.delayTime = 4
        self.update = update

    def write(self, dir, newData):
        sleep(self.delayTime)
        self.data[dir] = newData
        self.update(self)
        return

    def read(self, dir):
        sleep(self.delayTime)
        data = self.data[dir]
        return data