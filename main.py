import core
import connexion
import clock
import memory
from time import sleep

def printCore(intel):
    about = """ Core Info
    ID: {}
    Cache Info
\t|dir\t|tag\t|valid bit\t|data\t|""".format(intel.ID)
    print(about)
    for key in intel.myCache.datos:
        data = intel.myCache.datos[key]
        print("\t|{}\t|{}\t|{}\t|{}\t|".format(key,data[1],data[0],data[2]))

def printBus(bus):
    about = """Bus Info
    DIR: {}
    DATA: {}
    """.format(bus.dir, bus.data)
    print(about)

def printMem(memory):
    addresses = [*memory.data]
    addresses.sort()
    values = []
    for i in addresses:
        values.append(memory.data[i])
    about = """Memory Info
    Directions: {},
    Values:     {}
    """.format(addresses, values)
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

    print("Logging.... ")
    while(True):
        for i in cores:
            printCore(i)
        
        printBus(dataBus)
        printMem(mem)
        sleep(1)

        
simulation()       