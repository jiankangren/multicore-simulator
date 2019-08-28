from time import sleep
import threading
class clock (threading.Thread):
    play = True
    stop = False
    cicle = True
    countCicle = 0
    timeCicle = 1
    
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while(not self.stop):
            if(self.play):
                self.cicle = not self.cicle
                self.countCicle += 1
                sleep(self.timeCicle)
                print('cicle: {}'.format(self.cicle))


