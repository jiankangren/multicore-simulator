from tkinter import *
from tkinter import ttk
import time
import tkinter.scrolledtext as tkscrolled
from main import simulation

class core_gui:
    def __init__(self, parent, color, position, ID):
        self.space = parent
        self.color = color
        self.Cprocessor = Canvas(parent, width=250, height=110, bg = "light "+color)
        self.Clog = Canvas(parent, width=250, height=70, bg = "light "+color)
        self.Ccache = Canvas(parent, width=250, height=150, bg = "light "+color)
        x,y = position
        self.Cprocessor.place(x=x, y=y)
        self.Clog.place(x=x,y=y+115)
        self.Ccache.place(x=x, y=y+190)
        self.set_cache()
        self.set_core(ID)
        self.set_log()
    
    def change_color_state(self, state):
        color  = 'grey' 
        if(state == 'AWAKE'):
            color = self.color
        self.Cprocessor.itemconfig(self.edge, outline = color)

    def set_log(self):
        self.log = tkscrolled.ScrolledText(self.Clog, font=('Agency FB',8))
        self.log.place(x=5, y=5, width=240, height=60)

    def add_log(self,new_log):
        self.log.insert(END,new_log)
        self.log.see("end")


    def set_core(self,ID):
        self.edge = self.Cprocessor.create_rectangle(1,1,250,110, width = 10, outline=self.color)#'grey')#
        self.core_info = {}
        self.log = True
        miss = StringVar()
        hit = StringVar()
        mem = StringVar()
        total = StringVar()
        state = StringVar()
    
        self.core_info['miss']=miss
        self.core_info['hit']=hit
        self.core_info['mem']=mem
        self.core_info['total']=total
        self.core_info['state']=state
        self.core_info['log_fn']=self.add_log
        self.core_info['change_color']=self.change_color_state
        
        
        L_id = Label(self.Cprocessor, font=('Agency FB',8), text = "Core: ID"+str(ID), bg = "white", borderwidth=1, relief="groove")
        L_miss = Label(self.Cprocessor, font=('Agency FB',8), text = "Miss Rate:", bg = "white", borderwidth=1, relief="sunken")
        L_hit = Label(self.Cprocessor, font=('Agency FB',8), text = "Hit Rate:", bg = "white", borderwidth=1, relief="sunken")
        L_total = Label(self.Cprocessor, font=('Agency FB',8), text = "Local Total:", bg = "white", borderwidth=1, relief="sunken")
        L_mem = Label(self.Cprocessor, font=('Agency FB',8), text = "Mem Access:", bg = "white", borderwidth=1, relief="sunken")
        
        L_state = Label(self.Cprocessor, font=('Agency FB',8), text = "Current state:", bg = "white", borderwidth=1, relief="sunken")
        

        L_id.place(x=75, y=8, width = 55)    
        x,y = 15,28
        ancho = 75
        ancho2 = 40
        L_miss.place(x=x, y=y, width = ancho)
        E_miss = Entry(self.Cprocessor, font=('Agency FB',8), textvariable=miss, state='readonly')
        E_miss.place(x=x+ancho, y=y, width=ancho2)
        
        y+=16
        L_hit.place(x=x, y=y, width = ancho)
        E_hit = Entry(self.Cprocessor, font=('Agency FB',8), textvariable=hit, state='readonly')
        E_hit.place(x=x+ancho, y=y, width=ancho2)
        
        y+=16
        L_mem.place(x=x, y=y, width = ancho)
        E_mem = Entry(self.Cprocessor, font=('Agency FB',8), textvariable=mem, state='readonly')
        E_mem.place(x=x+ancho, y=y, width=ancho2)
        
        y+=16
        L_total.place(x=x, y=y, width = ancho)
        E_total = Entry(self.Cprocessor, font=('Agency FB',8), textvariable=total, state='readonly')
        E_total.place(x=x+ancho, y=y, width=ancho2)
        x,y = 132, 28
        L_state.place(x=x,y=y,width=110)
        
        y+=16
        x2=x+110-ancho2-5
        E_state = Entry(self.Cprocessor, font=('Agency FB',8), textvariable=state, state='readonly')
        E_state.place(x=x2, y=y, width = ancho2+5)
        y+=16
        btn_log = Button(self.Cprocessor,text="LOG", command = self.toggle_log, bg = self.color, fg = 'light grey', font=('Agency FB',8))
        btn_log.place(x=x+10,y=y)
    
    def toggle_log(self):
        self.log = not self.log
        self.core_info['log']=self.log
        

    def set_cache(self):
        y = 23
        L_dire = Label(self.Ccache, font=('Agency FB',8), text = "dir", bg = "white", borderwidth=1, relief="sunken")
        L_tag = Label(self.Ccache, font=('Agency FB',8), text = "tag", bg = "white", borderwidth=1, relief="sunken")
        L_valid = Label(self.Ccache, font=('Agency FB',8), text = "mesi", bg = "white", borderwidth=1, relief="sunken")
        L_data = Label(self.Ccache, font=('Agency FB',8), text = "data", bg = "white", borderwidth=1, relief="sunken")
        
        L_dire.place(x = 6, y = 3, width=55)
        L_tag.place(x = 68, y = 3, width=55)
        L_valid.place(x = 130, y = 3, width=55)
        L_data.place(x = 192, y = 3, width=55)
        
        self.cache_info = []
        for i in range(1,9):
            x = 3
            line_info = {}
            
            tag = StringVar()
            valid = StringVar()
            data = StringVar() 

            line_info['tag'] = tag
            line_info['valid'] = valid
            line_info['data'] = data
            
            self.cache_info.append(line_info)

            temp = Entry(self.Ccache, font=('Agency FB',8))
            temp.insert(END, str(hex(i-1)))
            temp.configure(state='readonly')
            temp.place(x=x, y=y, width=60)
            x+=62
            temp = Entry(self.Ccache, font=('Agency FB',8), textvariable=tag, state='readonly')
            temp.place(x=x, y=y, width=60)
            x+=62
            temp = Entry(self.Ccache, font=('Agency FB',8), textvariable=valid, state='readonly')
            temp.place(x=x, y=y, width=60)
            x+=62
            temp = Entry(self.Ccache, font=('Agency FB',8), textvariable=data, state='readonly')
            temp.place(x=x, y=y, width=60)
            y+=15

    def get_vars(self):
        return self.core_info, self.cache_info

            
class bus_gui:
    def __init__(self, parent, position):
        self.Cbus = Canvas(parent, bg ='snow', width = 768, height = 30) #width = 1024 * 3/4
        x,y=position
        self.Cbus.place(x=x, y=y)
        self.dir = StringVar()
        self.data = StringVar()
        
        L_dir = Label(self.Cbus, font=('Agency FB',10), text = "Current DIR on the bus:", bg='white', borderwidth=1, relief="sunken")
        L_dir.place(x=100,y=5, width=175)
        
        L_data = Label(self.Cbus, font=('Agency FB',10), text = "Current DATA on the bus:", bg='white', borderwidth=1, relief="sunken")
        L_data.place(x=350,y=5, width=175)
        
        E_dir = Entry(self.Cbus, font=('Agency FB',10), textvariable=self.dir, state='readonly')
        E_dir.place(x= 280, y=5, width=60)
        
        E_data = Entry(self.Cbus, font=('Agency FB',10), textvariable=self.data, state='readonly')
        E_data.place(x= 530, y=5, width=60)

class memory_gui:
    def __init__(self, parent, position ):
        self.Cmemory = Canvas(parent, bg = 'light yellow', width = 890, height = 70)
        x,y=position
        self.Cmemory.place(x=x,y=y)
        L_title = Label(self.Cmemory, font=('Agency FB',10), text = "MAIN MEMORY", bg='white', borderwidth=1, relief="groove")
        L_title.place(x=57,y=2)
        L_dir = Label(self.Cmemory, font=('Agency FB',8), text = "DIR ", bg='white', borderwidth=1, relief="groove")
        L_dir.place(x=5,y=25, width = 50)
        L_data = Label(self.Cmemory, font=('Agency FB',8), text = "DATA", bg='white', borderwidth=1, relief="groove")
        L_data.place(x=5,y=45, width = 50)
        self.set_data()
    
    def set_data(self):
        self.data = {}
        for i in range(1,17):
            L_dir = Label(self.Cmemory, font=('Agency FB',8), text = str(hex(i-1)), bg='white', borderwidth=1, relief="sunken")
            L_dir.place(x=5+52*i,y=25, width = 50)
            str_pos = StringVar(value='mem')
            self.data[i-1]=str_pos
            temp = Entry(self.Cmemory, font=('Agency FB',8), textvariable=str_pos, state='readonly')
            temp.place(x=5+52*i,y=45, width = 50)


        # L_data = Label(self.Cmemory, font=('Agency FB',8), text = "DATA", bg='white', borderwidth=1, relief="groove")
        # L_data.place(x=5,y=45, width = 50)
        
        
class main_view:
    general = {}
    mem_dic = {}
    bus_dic = {}
    core_dic_list = []
    cache_dic_list = []
    
    def __init__(self, simulation):
        self.simulation = simulation
        self.root = Tk()

        self.root.title('Arquitectura de Computadores 2, Proyecto Programado 1')
        self.root.minsize(1024,600)
        self.root.resizable(width=NO,height=NO)

        C_root = Canvas(self.root,bg='white')
        C_root.pack(fill=BOTH, expand=1)
        x, y = 4,460
        bus = bus_gui(C_root, (x+128,y))
        self.bus_dic['dir'] = bus.dir
        self.bus_dic['data'] =  bus.data

        y += 50
        mem = memory_gui(C_root, (x+60,y))
        self.mem_dic = mem.data

        x, y = 4,100
        for color in ('blue', 'green', 'cyan', 'salmon'):
            new = core_gui(C_root, color, (x,y), len(self.core_dic_list))
            core_vars, cache_vars = new.get_vars()
            self.core_dic_list.append(core_vars)
            self.cache_dic_list.append(cache_vars)
            x += 250

        x=300
        L_temp = Label(C_root, font=('Agency FB',10), text = "Frequency:", bg='white', borderwidth=1, relief="sunken")
        L_temp.place(x=x,y=50)

        x+=77
        temp = Entry(C_root, font=('Agency FB',10))
        temp.insert(END,"{}Hz".format(1/1))
        temp.configure(state='readonly')
        temp.place(x=x,y=50, width = 50)

        x+=55
        L_temp = Label(C_root, font=('Agency FB',10), text = "Cicles Count:", bg='white', borderwidth=1, relief="sunken")
        L_temp.place(x=x,y=50)

        x+=90
        cicles = StringVar()
        self.general['cicles']= cicles
        temp = Entry(C_root, font=('Agency FB',10), state='readonly', textvariable = cicles)
        temp.place(x=x,y=50, width = 50)

        x+=55
        L_freq = Label(C_root, font=('Agency FB',10), text = "Total Instructions:", bg='white', borderwidth=1, relief="sunken")
        L_freq.place(x=x,y=50)

        x+=122
        total = StringVar()
        self.general['total'] = total
        temp = Entry(C_root, font=('Agency FB',10), state='readonly', textvariable = total)
        temp.place(x=x,y=50, width = 50)

        x=10 
        Btn_start = Button(C_root,text='START',command=self.start,fg='black',bg='yellow', font=('Agency FB',12))
        Btn_start.place(x=x,y=50)

        x=+100
        Btn_play = Button(C_root,text='PLAY',command=self.play,fg='black',bg='yellow', font=('Agency FB',12))
        Btn_play.place(x=x,y=50)

        x+=75 
        Btn_play = Button(C_root,text='PAUSE',command=self.pause,fg='black',bg='yellow', font=('Agency FB',12))
        Btn_play.place(x=x,y=50)

        self.simulation.add_dictionaries(self.general, self.core_dic_list, self.cache_dic_list, self.mem_dic, self.bus_dic)


    def start(self):
        self.simulation.start()
        self.mainloop()

    def play(self):
        self.simulation.play()
        self.mainloop()

    def pause(self):
        self.simulation.pause()


    def mainloop(self):
        self.root.mainloop()



sim = simulation()
view = main_view(sim)
view.mainloop()



