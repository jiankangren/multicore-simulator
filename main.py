import core
import connexion
import clock
import memory
from time import sleep

def printCore(intel):
    about = """ Core Info
    ID: {}
    STATE: {}
    Cache Info
\t|dir\t|tag\t|valid bit\t|data\t|"""\
    .format(intel.ID, intel.processor.state)
    
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


def simulation():
    mem = memory.memory()
    dataBus = connexion.bus(mem)
    clk = clock.clock()
    cores = []
    core1 = core.core('id1',dataBus,clk)
    core2 = core.core('id2',dataBus,clk)
    cores.append(core1)
    cores.append(core2)
    clk.start()
    logging = True
    if(logging):
        print("Logging.... ")    
        count = 0
        while(True):
            if(clk.countCicle != count):
                count = clk.countCicle
                for i in cores:
                    printCore(i)
                
                printBus(dataBus)
                printMem(mem)
            
            else:
                sleep(0.5)

        
simulation()       