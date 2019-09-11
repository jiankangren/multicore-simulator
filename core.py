import connexion
import cache
import cacheController
from time import sleep
import threading
import random



class core:
    isa = ['read','process','write']
    class processor (threading.Thread):
        state = 'AWAKE'
        def __init__(self, coreID, clk, ctrCache):
            self.ID = coreID
            self.clock = clk
            self.processTime = 1
            self.ctrCache = ctrCache
            self.standby = threading.Condition()
            self.ctrCache.add_pause(self.standby)
            threading.Thread.__init__(self)

        def process(self):
            sleep(self.processTime)
       

        def run(self):
            count = self.clock.countCicle
            while(True):
                if(count != self.clock.countCicle ):
                    count = self.clock.countCicle
                    instr = core.generateInstruction()
                    command = """### NEW INSTRUCTION ###\n\tCORE ID:    {}\n\tTYPE:\t{}"""\
                    .format(self.ID, instr)
                    if(instr in ['read', 'write']):
                        dir = random.randrange(16)
                        command+="\n\tDIR:\t{}".format(dir)
                        print(command)
                        if (instr == 'read'):
                            self.ctrCache.read(dir)

                        elif (instr == 'write'):
                            self.ctrCache.write(dir, self.ID)
                            

                    elif (instr == 'process'):
                        print(command)
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
            return core.isa[random.randrange(3)] ### SHOULD BE 3
