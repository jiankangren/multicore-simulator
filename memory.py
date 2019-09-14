from time import sleep

class memory:
    data = {
        0x0:'0',#
        0x1:'0',#
        0x2:'0',#
        0x3:'0',#
        0x4:'0',#
        0x5:'0',#
        0x6:'0',#
        0x7:'0',# 
        0x8:'0',#
        0x9:'0',#
        0xA:'0',#
        0xB:'0',#
        0xC:'0',#
        0xD:'0',#
        0xE:'0',#
        0xF:'0' #        
        }
    size = 16

    def __init__(self, update):
        self.delayTime = 3
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