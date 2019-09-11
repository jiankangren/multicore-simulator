from time import sleep

class cache:
    size = 8
    def __init__(self):
        self.datos = {
        ### dir: [valid bit, tag, data]
            0x0:['invalid',0,'0'],#
            0x1:['invalid',0,'0'],#
            0x2:['invalid',0,'0'],#
            0x3:['invalid',0,'0'],#
            0x4:['invalid',0,'0'],#
            0x5:['invalid',0,'0'],#
            0x6:['invalid',0,'0'],#
            0x7:['invalid',0,'0'] #
        }

        self.delayTime = 1.5

    
    def read(self, dir):
        sleep(self.delayTime)
        return self.datos[dir][2]

    def write(self, dir, state, tag, data):
        sleep(self.delayTime)
        self.datos[dir] = [state, tag, data]
    
    def get_valid(self, dir):
        return self.datos[dir][0]
    
    def get_tag(self, dir):
        return self.datos[dir][0]

    def change_state(self, dir, state):
        self.datos[dir][0] = state

    def directions(self):
        return self.datos.keys()