import core
import connexion
import clock
import memory
from time import sleep

def printCore(intel):
    miss, hit, mem, total = intel.get_rates()
    
    about = """ Core Info
    ID: {}
    STATE: {}
    Miss Rate: {}%
    Hit Rate: {}%
    Memory Access: {}%
    Total: {}
    Cache Info
\t|dir\t|tag\t|valid bit\t|data\t|"""\
    .format(intel.ID, intel.state, round(miss,4), round(hit,4), round(mem,4), total)
    
    print(about)
    for key in intel.myCache.datos:
        data = intel.myCache.datos[key]
        print("\t|{}\t|{}\t|{}\t|{}\t|".format(hex(key),data[1],data[0],data[2]))

def printBus(bus):
    about = """Bus Info
    DIR: {}
    DATA: {}
    """.format(bus.dir, bus.data)
    print(about)

def printMem(memory):
    dir = [*memory.data]
    dir.sort()
    str_dir = ""
    str_data = ""
    for i in dir:
        str_dir += "|"+str(hex(i))+"\t"
        str_data += "|"+memory.data[i]+"\t"
    
    str_dir += "|"
    str_data += "|"
    
    about = """Memory Info
    DIR:  {}
    DATA: {}
    """.format(str_dir, str_data)
    print(about)


class simulation:

    def __init__(self):
        self.running = False 
        self.mem = memory.memory(self.update_view)
        self.dataBus = connexion.bus(self.mem, self.update_view)
        self.clk = clock.clock(self.update_clock)
        self.cores_list = []
        self.local_total_list=[0,0,0,0]
        for i in range(4):
            self.cores_list.append(core.core(i,self.dataBus,self.clk,self.update_core))
    
    def get_freq(self):
        return round(1/self.clk.timeCicle,4)

    def add_dictionaries(self, general, core_dic_list, cache_dic_list, mem_dic, bus_dic):
        self.general_vars = general
        self.cores_vars = core_dic_list
        self.cache_vars = cache_dic_list
        self.mem_vars = mem_dic
        self.bus_vars = bus_dic
    
    def update_clock(self, count):
        self.general_vars['cicles'].set(str(count))

    def update_state(self, index):
        state = self.cores_list[index].state
        self.cores_vars[index]['state'].set(state)

    def update_view(self, obj):
        objType = obj.__class__.__name__
        if(objType == '__bus'):
            self.update_bus(obj)

        elif (objType == 'memory'):
            self.update_mem(obj)
    
    def update_core(self, id, tipo):
        if(tipo == 'rates'):
            self.update_rates(id)
        elif (tipo == 'state'):
            self.update_state(id)
        elif(tipo == 'cache'):
            self.update_cache(id)

    

    def update_cache(self, index):
        for dir in self.cores_list[index].myCache.datos.keys():
            valid, tag, data =  self.cores_list[index].myCache.datos[dir]
            self.cache_vars[index][dir]['tag'].set(tag)
            self.cache_vars[index][dir]['valid'].set(valid)
            self.cache_vars[index][dir]['data'].set(data)
            

    def update_rates(self, index):
        intel = self.cores_list[index]
        core_dict = self.cores_vars[index]
        print(self.cores_vars[index].keys())
        miss, hit, mem, total = intel.get_rates()
        self.local_total_list[index] = total
        sum = 0
        for i in self.local_total_list:
            sum+=i
        self.general_vars['total'].set(str(sum))

        core_dict['state'].set(intel.state)
        core_dict['miss'].set(str(round(miss,4)))
        core_dict['hit'].set(str(round(hit,4)))
        core_dict['mem'].set(str(round(mem,4)))
        core_dict['total'].set(str(total))
        # if(core_dict['log'] != intel.log):
        #     intel.log = core_dict['log']

    
    def update_bus(self, bus):
        self.bus_vars['data'].set(bus.data)
        self.bus_vars['dir'].set(str(bus.dir))

    def update_mem(self, mem):
        for dir in mem.data:
            self.mem_vars[dir].set(mem.data[dir])


    def start(self):
        if(not self.running):
            print("start simulation")
            self.running = True
            self.clk.start()
            self.dataBus.start()
            for core in self.cores_list:
                core.start()
            self.play()

    def pause(self):
        self.clk.pause()
    
    def play(self):
        self.clk.go()



#     mem = memory.memory()
#     dataBus = connexion.bus(mem)
#     clk = clock.clock()
#     cores = []
#     for i in range(4):
#         id='id'+str(i+1)
#         cores.append(core.core(id,dataBus,clk))
        
#     clk.start()
#     logging = True
#     if(logging):
#         print("Logging.... ")    
#         count = 0
#         while(True):
#             if(clk.countCicle != count):
#                 count = clk.countCicle
#                 for i in cores:
#                     printCore(i)
                
#                 printBus(dataBus)
#                 printMem(mem)
            
#             else:
#                 sleep(0.5)

        
# simulation()       