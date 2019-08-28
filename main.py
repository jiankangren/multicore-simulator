import core
import connexion
import clock

def simulation():
    dataBus = connexion.bus()
    clk = clock.clock()
    cores = []
    core1 = core.core('id1',dataBus,clk)
    core2 = core.core('id2',dataBus,clk)
    cores.append(core1)
    cores.append(core2)
    clk.start()

simulation()      