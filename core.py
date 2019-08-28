import connexion
import cache
import cacheController
from time import sleep
import threading
import random



class core:
    isa = ['read','write','process']

    class processor (threading.Thread):

        def __init__(self, coreID, clk, ctrCache):
            self.ID = coreID
            self.clock = clk
            self.processTime = 10
            self.ctrCache = ctrCache
            threading.Thread.__init__(self)

        def process(self):
            print(self.ID+'>>processing')
            sleep(self.processTime)
       

        def run(self):
            count = self.clock.countCicle
            while(True):
                if(count != self.clock.countCicle ):
                    count = self.clock.countCicle
                    instr = core.generateInstruction()
                    if (instr == 'read'):
                        print(self.ID+'>>reading')

                    elif (instr == 'write'):
                        print(self.ID+'>>writing')

                    elif (instr == core.isa[2]):
                        self.process()
                
                else:
                    sleep(1)




    def __init__(self, coreID, bus, clock):
        myBus = connexion.bus()
        myCache = cache.cache()
        controller = cacheController.controller(myBus, myCache)
        self.processor = core.processor(coreID, clock, controller)
        self.processor.start()
        
    @staticmethod
    def generateInstruction():
            return core.isa[random.randrange(3)]
    

