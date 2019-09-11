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
            self.processTime = 1
            self.ctrCache = ctrCache
            self.standby = threading.Condition()
            self.ctrCache.add_pause(self.standby)
            threading.Thread.__init__(self)

        def process(self):
            print(self.ID+'>> Processing')
            sleep(self.processTime)
       

        def run(self):
            count = self.clock.countCicle
            while(True):
                if(count != self.clock.countCicle ):
                    count = self.clock.countCicle
                    instr = core.generateInstruction()

                    if(instr in ['read', 'write']):
                        with self.standby:
                            if (instr == 'read'):
                                dir = random.randrange(16)
                                print(self.ID+'>> reading to', dir)
                                self.ctrCache.read(dir)

                            elif (instr == 'write'):
                                dir = random.randrange(16)
                                print(self.ID+'>> writing to', dir)
                                self.ctrCache.write(dir, self.ID)
                            
                            self.standby.wait()

                    elif (instr == 'process'):
                        self.process()
                
                else:
                    sleep(0.5)


    def __init__(self, coreID, bus, clock):
        self.ID = coreID
        self.myBus = bus
        self.myCache = cache.cache()
        self.controller = cacheController.controller(self.myCache, self.myBus)
        self.myBus.add_ctrl(self.controller)
        self.processor = core.processor(coreID, clock, self.controller)
        self.processor.start()
        
    @staticmethod
    def generateInstruction():
            return core.isa[random.randrange(3)]
