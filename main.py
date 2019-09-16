import core
import connexion
import clock
import memory
from time import sleep

class simulation:

    def __init__(self):
        self.log = [[],[],[],[]]
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
        self.cores_vars[index]['change_color'](state)
        
    def add_log(self,id, log_entry):
        fn_log = self.cores_vars[id]['log_fn']
        fn_log(log_entry)

    def update_view(self, obj):
        objType = obj.__class__.__name__
        if(objType == '__bus'):
            self.update_bus(obj)

        elif (objType == 'memory'):
            self.update_mem(obj)
    
    def update_core(self, id, tipo, log = ''):
        if(tipo == 'rates'):
            self.update_rates(id)
        elif (tipo == 'state'):
            self.update_state(id)
        elif(tipo == 'cache'):
            self.update_cache(id)
        elif(tipo == 'log'):
            self.add_log(id, log)
            
    

    def update_cache(self, index):
        for dir in self.cores_list[index].myCache.datos.keys():
            valid, tag, data =  self.cores_list[index].myCache.datos[dir]
            self.cache_vars[index][dir]['tag'].set(tag)
            self.cache_vars[index][dir]['valid'].set(valid)
            self.cache_vars[index][dir]['data'].set(data)
            

    def update_rates(self, index):
        intel = self.cores_list[index]
        core_dict = self.cores_vars[index]
      
        miss, hit, mem, total = intel.get_rates()
        self.local_total_list[index] = total
        sum = 0
        for i in self.local_total_list:
            sum+=i
        self.general_vars['total'].set(str(sum))

        core_dict['state'].set(intel.state)
        core_dict['miss'].set(str(round(miss,2)))
        core_dict['hit'].set(str(round(hit,2)))
        core_dict['mem'].set(str(round(mem,2)))
        core_dict['total'].set(str(total))
        # if(core_dict['log'] != intel.log):
        #     intel.log = core_dict['log']

    
    def update_bus(self, bus):
        self.bus_vars['data'].set(bus.data)
        self.bus_vars['dir'].set(str(hex(bus.get_dir())))

    def update_mem(self, mem):
        for dir in mem.data:
            self.mem_vars[dir].set(mem.data[dir])


    def start(self):
        if(not self.running):
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
