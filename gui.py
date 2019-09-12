from tkinter import *
from tkinter import ttk
import core
import time

class core_gui:
    def __init__(self, parent, core, color, position):
        self.core = core
        self.space = parent
        self.color = color
        self.Cprocessor = Canvas(parent, width=250, height=110, bg = "light "+color)
        self.Ccache = Canvas(parent, width=250, height=150, bg = "light "+color)
        x,y = position
        self.Cprocessor.place(x=x, y=y)
        self.Ccache.place(x=x, y=y+115)
        self.set_cache()
        self.set_core()

    def set_core(self):
        self.Cprocessor.create_rectangle(1,1,250,110, width = 10, outline='grey')#self.color)
        self.core_info = {}
        miss = StringVar(value="99%")
        hit = StringVar(value="1%")
        mem = StringVar(value="5%")
        total = StringVar(value="20")
        instr = StringVar(value="read")
    
        self.core_info['miss']=miss
        self.core_info['hit']=hit
        self.core_info['mem']=mem
        self.core_info['total']=total
        self.core_info['instr']=instr
        
        
        L_id = Label(self.Cprocessor, font=('Agency FB',8), text = "Core: "+("ID1"), bg = "white", borderwidth=1, relief="groove")
        L_miss = Label(self.Cprocessor, font=('Agency FB',8), text = "Miss Rate:", bg = "white", borderwidth=1, relief="sunken")
        L_hit = Label(self.Cprocessor, font=('Agency FB',8), text = "Hit Rate:", bg = "white", borderwidth=1, relief="sunken")
        L_total = Label(self.Cprocessor, font=('Agency FB',8), text = "Total:", bg = "white", borderwidth=1, relief="sunken")
        L_mem = Label(self.Cprocessor, font=('Agency FB',8), text = "Mem Access:", bg = "white", borderwidth=1, relief="sunken")
        
        L_instr = Label(self.Cprocessor, font=('Agency FB',8), text = "Current Instruction:", bg = "white", borderwidth=1, relief="sunken")
        

        L_id.place(x=70, y=8, width = 50)    
        x,y = 15,28
        ancho = 75
        ancho2 = 40
        L_miss.place(x=x, y=y, width = ancho)
        temp = Entry(self.Cprocessor, font=('Agency FB',8), textvariable=miss, state='readonly')
        temp.place(x=x+ancho, y=y, width=ancho2)
        y+=16
        L_hit.place(x=x, y=y, width = ancho)
        temp = Entry(self.Cprocessor, font=('Agency FB',8), textvariable=hit, state='readonly')
        temp.place(x=x+ancho, y=y, width=ancho2)
        y+=16
        L_mem.place(x=x, y=y, width = ancho)
        temp = Entry(self.Cprocessor, font=('Agency FB',8), textvariable=mem, state='readonly')
        temp.place(x=x+ancho, y=y, width=ancho2)
        y+=16
        L_total.place(x=x, y=y, width = ancho)
        temp = Entry(self.Cprocessor, font=('Agency FB',8), textvariable=total, state='readonly')
        temp.place(x=x+ancho, y=y, width=ancho2)
        x,y = 132, 28
        L_instr.place(x=x,y=y,width=110)
        y+=16
        x2=x+110-ancho2
        temp = Entry(self.Cprocessor, font=('Agency FB',8), textvariable=instr, state='readonly')
        temp.place(x=x2, y=y, width = ancho2)
        y+=16
        btn_log = Button(self.Cprocessor,text="LOG", command = self.log, bg = self.color, fg = 'light grey', font=('Agency FB',8))
        btn_log.place(x=x+10,y=y)
    
    def log(self):
        pass


    def set_cache(self):
        y = 23
        L_dire = Label(self.Ccache, font=('Agency FB',8), text = "dir", bg = "white", borderwidth=1, relief="sunken")
        L_tag = Label(self.Ccache, font=('Agency FB',8), text = "tag", bg = "white", borderwidth=1, relief="sunken")
        L_valid = Label(self.Ccache, font=('Agency FB',8), text = "msi", bg = "white", borderwidth=1, relief="sunken")
        L_data = Label(self.Ccache, font=('Agency FB',8), text = "data", bg = "white", borderwidth=1, relief="sunken")
        
        L_dire.place(x = 6, y = 3, width=55)
        L_tag.place(x = 68, y = 3, width=55)
        L_valid.place(x = 130, y = 3, width=55)
        L_data.place(x = 192, y = 3, width=55)
        
        self.cache_info = []
        for i in range(1,9):
            x = 3
            line_info = {}

            dire = StringVar(value='0x10')
            tag = StringVar(value='0')
            valid = StringVar(value='invalid')
            data = StringVar(value='0') 
            
            line_info['dir'] = dire
            line_info['tag'] = tag
            line_info['valid'] = valid
            line_info['data'] = data
        
            temp = Entry(self.Ccache, font=('Agency FB',8), textvariable=dire, state='readonly')
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
            

root = Tk()


root.title('Arquitectura de Computadores 2, Proyecto Programado 1')
root.minsize(1024,600)
root.resizable(width=NO,height=NO)

C_root = Canvas(root,bg='white')
C_root.pack(fill=BOTH, expand=1)
x=4
new = core_gui(root, None, 'blue', (x,75))
new = core_gui(root, None, 'green', (x+255,75))
new = core_gui(root, None, 'cyan', (x+510,75))
new = core_gui(root, None, 'salmon', (x+765,75))

root.mainloop()
