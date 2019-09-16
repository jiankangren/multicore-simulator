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
        def __init__(self, coreID, clk, ctrCache, update):
            self.ID = coreID
            self.clock = clk
            self.ctrCache = ctrCache
            self.standby = threading.Condition()
            self.ctrCache.add_pause(self.standby)
            self.update = update 
            threading.Thread.__init__(self)

        def process(self):
            sleep(self.processTime)
            self.update(self.ID,'rates')
       

        def run(self):
            while(True):
                if( self.clock.play ):
                    
                    instr = core.generateInstruction()
                    self.instr_count += 1
                    command = "$ Cicle:{} Intruction:{}->\n >>> {} ".format(self.clock.countCicle, self.instr_count,instr)
                    if(instr in ['read', 'write']):
                        dir = random.randrange(16)
                        command+="DIR:{} DATA:ID{}\n".format(dir,self.ID)
                        self.update(self.ID, 'log', log=command)

                        if (instr == 'read'):
                            self.ctrCache.read(dir)

                        elif (instr == 'write'):
                            self.ctrCache.write(dir, "ID{}".format(self.ID))        

                    elif (instr == 'process'):
                        command+="\n"
                        self.update(self.ID, 'log', log=command)
                        self.process()

                
                else:
                    sleep(0.5)


    def __init__(self, coreID, bus, clock, update):
        self.ID = coreID
        self.myBus = bus
        self.update = update
        self.myCache = cache.cache(coreID, update)
        self.controller = cacheController.controller(self.myCache, self.myBus, self.change_state, update, coreID)
        self.myBus.add_ctrl(self.controller)
        self.processor = core.processor(coreID, clock, self.controller, update)
    
    def start(self):
         self.processor.start()

    def change_state(self, state):
        self.state = state
        self.update(self.ID, 'state')

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
