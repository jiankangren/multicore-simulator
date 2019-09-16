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

        def __init__(self, mem, update):
            self.memory = mem
            self.update = update
            self.p = threading.Thread(target=self.operations)
        
        def start(self):
            self.p.start()

        ### PUT WRITE OP IN QUEUE
        def request_write(self, condition, dir, data):
            req = (condition, self.read_mem,[dir, data], 0)
            self.requestQ.put(req)

        ### PUT READ OP IN QUEUE
        def request_read(self, condition, dir, id):
            req = (condition, self.read_data, [dir, id], 1)
            self.requestQ.put(req)

        ### PUT WRITE OP IN PRIORITY QUEUE
        def write_back(self, dir, data):
            p_req = (self.write_mem, [dir, data])
            self.priorityQ.put(p_req)


        def read_data(self, dir, id):
            ### ASK CORES FOR DATA
            inCache = False
            for ctrl in self.cacheCtrl_array:
                inCache = ctrl.notify_read(id, dir)
                if(inCache):
                    break
                    
            ### IF CORES DON'T HAVE IT CALL MEMORY
            if(not inCache):
                self.read_mem(dir)
        

        def set_data(self, data, id):
            #print("change data from {}".format(id))
            self.data = data
            self.update(self)

        def get_data(self):
            return self.data

        def set_dire(self, dir):
            self.dir = dir
            self.update(self)
        
        def get_dir(self):
            return self.dir

        def add_ctrl(self, core):
            self.cacheCtrl_array.append(core)

        def read_mem(self, dir):
            self.dir = dir
            self.set_data(self.memory.read(dir), "Mem")
        
        def notify_cores(self, dir, id):
            for ctrl in self.cacheCtrl_array:
                self.dir_miss = dir
                ctrl.notify_write(dir,  id)

        def write_mem(self, dir, data):
            self.dir = dir
            self.memory.write(dir, data)
        
        def operations(self):
            while(1):
                if(self.priorityQ.empty()):
                    if(not self.requestQ.empty()):
                        #print("QUEUE MEMORY OPERATIONS SIZE:{}".format(self.requestQ.qsize()))
                        condi, fn, args, read = self.requestQ.get()
                        with condi:
                            fn(*args)
                            self.update(self)
                            condi.notify()
                            if(read):
                                condi.wait()
                                
                    else:
                        ### IF there is no READ/WRITE OPERATION
                        sleep(0.5)
                else:
                    #print("QUEUE PRIORITY MEMORY OPERATIONS SIZE:{}".format(self.priorityQ.qsize()))
                    fn, args = self.priorityQ.get()
                    fn(*args)
                    self.update(self)
               
    instance = None
    def __init__(self, mem, update):
        if(not bus.instance):
            bus.instance = bus.__bus(mem, update)
    
    def __getattr__(self, name):
        return getattr(self.instance, name)


