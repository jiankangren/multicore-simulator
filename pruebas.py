import time
import queue
import threading
import random

cont = 0

class bus:
    myq = queue.Queue()
    inBus = None
    mem = {
        0:'Cero',
        1:'Uno',
        2:'Dos',
        3:'Tres',
        4:'Cuatro',
        5:'Cinco',
        6:'Seis',
        7:'Siete',
        8:'Ocho',
        9:'Nueve'
        }
    def __init__(self):
        A = threading.Thread(target=self.monitor)
        A.start()

    def monitor(self):
        while(1):
            if(not self.myq.empty()):
                print("not empty")
                i,condi = self.myq.get()
                with condi:
                    print("Managing", i)
                    self.inBus = self.read_mem(i)
                    condi.notify()
            time.sleep(0.5)
            
    def read_mem(self, i):
        time.sleep(5)
        return self.mem[i]

    def request(self, i, condi):
        self.myq.put((i, condi))
        print("Request QUEUED", i)
    
    def read(self):
        return self.inBus

miBus = bus()

def leerfoo(id, bus):
    standby = threading.Condition()
    while(1):
        i = random.randrange(10)
        with standby:
            bus.request(i, standby)
            print("STANDBY", id)
            standby.wait()
            print("WAKE UP", id)
            a = bus.read()
        print("HI! from: {}\nRead: {}".format(id,a))
    

p = threading.Thread(target=leerfoo, args=(1,miBus))
p.start()
s = threading.Thread(target=leerfoo, args=(2, miBus))
s.start()

p.join()
s.join()