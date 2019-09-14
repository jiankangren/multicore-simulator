from time import sleep
import threading
class clock (threading.Thread):
    play = False
    stop = False
    cicle = True
    countCicle = 0
    timeCicle = 1
    
    def __init__(self, update):
        self.update = update
        threading.Thread.__init__(self)
    
    def pause(self):
        if(self.play):
            self.play = False

    def go(self):
        if(not self.play):
            self.play = True

    def run(self):
        while(not self.stop):
            if(self.play):
                self.cicle = not self.cicle
                self.countCicle += 1
                self.update(self.countCicle)
                sleep(self.timeCicle)
                #print('cicle: {}'.format(self.cicle))
            else:
                sleep(self.timeCicle/2)

