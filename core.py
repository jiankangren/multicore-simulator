import connexion
import cache
import cacheController
from time import sleep
import threading
import random



class core:
    isa = ['read','process','write']
    state = "AWAKE"
    
    class processor (threading.Thread):
        instr_count = 0
        processTime = 1
        def __init__(self, coreID, clk, ctrCache):
            self.ID = coreID
            self.clock = clk
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
                    self.instr_count += 1
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
        self.controller = cacheController.controller(self.myCache, self.myBus, self.change_state)
        self.myBus.add_ctrl(self.controller)
        self.processor = core.processor(coreID, clock, self.controller)
        self.processor.start()

    def change_state(self, state):
        self.state = state

    def get_rates(self):
        total = self.processor.instr_count
        missRate, hitRate, mem = 0,0,0
        if(total>0):
            miss_count = self.controller.missRate
            hit_count = self.controller.hitRate
            missRate = (miss_count/total)*100
            hitRate = (hit_count/total)*100
            mem = ((hit_count+miss_count)/total)*100

        return [missRate, hitRate, mem, total]

    @staticmethod
    def generateInstruction():
        ### Funcion con distribucion especial

            return core.isa[random.randrange(3)] ### SHOULD BE 3
