import threading 
import queue
from time import sleep

class bus:
    class __bus:
        data = 0
        dir = 0
        requestQ = queue.Queue()
        priorityQ = queue.Queue()
        cacheCtrl_array = []

        def __init__(self, mem):
            self.memory = mem
            p = threading.Thread(target=self.operations)
            p.start()
        ### PUT WRITE OP IN QUEUE
        def request_write(self, condition, dir, data):
            req = (condition, self.read_mem,[dir, data])
            self.requestQ.put(req)

        ### PUT READ OP IN QUEUE
        def request_read(self, condition, dir):
            req = (condition, self.read_data, [dir])
            self.requestQ.put(req)

        ### PUT WRITE OP IN PRIORITY QUEUE
        def write_back(self, dir, data):
            p_req = (self.write_mem, [dir, data])
            self.priorityQ.put(p_req)


        def read_data(self, dir):
            ### ASK CORES FOR DATA
            dataMem = True
            for ctrl in self.cacheCtrl_array:
                if(ctrl.notify_read()):
                    dataMem = False
                    break
            
            ### IF CORES DON'T HAVE IT CALL MEMORY
            if(dataMem):
                self.read_mem(dir)

        def add_ctrl(self, core):
            self.cacheCtrl_array.append(core)

        def read_mem(self, dir):
            self.dir = dir
            self.data = self.memory.read(dir)
        
        def notify(self, dir):
            self.dir = dir
            for ctrl in self.cacheCtrl_array:
                ctrl.notify_write()

        def write_mem(self, dir, data):
            self.dir = dir
            self.memory.write(dir, data)
        
        def operations(self):
            while(1):
                if(self.priorityQ.empty()):
                    if(not self.requestQ.empty()):
                        condi, fn, args = self.requestQ.get()
                        with condi:
                            fn(*args)
                            condi.notify()
                    else:
                        ### IF there is no READ/WRITE OPERATION
                        sleep(0.5)
                else:
                    fn, args = self.priorityQ.get()
                    fn(*args)
               
    instance = None
    def __init__(self, mem):
        if(not bus.instance):
            bus.instance = bus.__bus(mem)
    
    def __getattr__(self, name):
        return getattr(self.instance, name)


