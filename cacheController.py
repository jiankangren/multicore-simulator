class controller:

    hitRate = 0
    missRate = 0
    thread_pause = None
    
    def __init__(self, _cache, _bus, _state, update, coreID):
        self.cache = _cache
        self.cachesize = _cache.size
        self.bus = _bus
        self.core_state = _state
        self.ID = coreID
        self.update_view = update
    
    def map_dir(self,dir):
        ### Find the tag and cache address
        ### Can work with different cache and memory size
        ### Can be replaced with a big if module
        cachedir = dir
        tag = 0
        while (cachedir >= self.cachesize) :
            cachedir -= self.cachesize
            tag += 1
        return cachedir, tag
    

    def add_pause(self, pause):
        self.thread_pause = pause

    def read(self, dir):
        cachedir,tag = self.map_dir(dir)
        ### CHECK IF DATA IS IN CACHE
        cacheTag = self.cache.get_tag(cachedir)
        validbit = self.cache.get_valid(cachedir)
        miss = False
        if(validbit == 'invalid'):
            log = "$ CPU READ MISS INVALID dir:{}\n".format(hex(dir))
            self.update_view(self.ID, 'log', log=log)
            miss = True
         
        if(validbit == 'shared'):
            if(cacheTag != tag):
                log = "$ READ MISS TAG dir:{}\n".format(hex(dir))
                self.update_view(self.ID, 'log', log=log)
                miss = True

                
        if(validbit == 'modified'):
            if(cacheTag != tag):
                miss = True
                ### STORE DATA AT MEMORY (WRITE BACK)
                data = self.cache.read(cachedir)
                ### WRITE BACK DIR
                wb_dir = cachedir + self.cachesize*cacheTag
                ### UPDATING VIEW
                log = "$ WRITE BACK dir:{} data:{}\n".format(wb_dir,data)
                self.update_view(self.ID, 'log', log=log)
                self.bus.write_back(wb_dir, data)
            
        ### IF THERE IS A MISS
        ### ASK BUS AND STORE IN CACHE
        
        if(miss):
            #print("MISS READ")
            self.missRate += 1
            with self.thread_pause:
                ### ASK BUS FOR THE DATA 
                self.bus.request_read(self.thread_pause, dir, self.ID) 
                ### SLEEPS the core
                self.core_state('SLEEP')
                self.thread_pause.wait()
                self.core_state ('AWAKE')
                
                ### CACHE DATA      
                readed_data = self.bus.get_data()
                #print("readed data:",readed_data)
                self.cache.write(cachedir, 'shared', tag, readed_data)
                ### READY READ
                self.thread_pause.notify() 


        else:
            #print("HIT READ")
            log = "$ CPU READ HIT dir:{}\n".format(hex(dir))
            self.update_view(self.ID, 'log', log=log)
            self.hitRate += 1
        
        self.update_view(self.ID,'rates')
        return self.cache.read(cachedir)


    def write(self, dir, data):
        cachedir,tag = self.map_dir(dir)
        ### CHECK IF DATA IS IN CACHE
        cacheTag = self.cache.get_tag(cachedir)
        validbit = self.cache.get_valid(cachedir)
        ### 
        hit = True
        if(validbit == 'modified' or validbit == 'exclusive'):
            if(cacheTag != tag):
                ### SAVE MISS
                hit = False 
                log = "$ WRITE MISS TAG dir:{} tag: {}\n".format(cachedir, cacheTag)
                self.update_view(self.ID, 'log', log=log)    
                ### SAVE DATA IN MEMORY
                data = self.cache.read(cachedir)
                ### WRITE BACK THE DATA
                log = "$ WRITE BACK dir:{} data:{}\n".format(hex(dir), data)
                self.update_view(self.ID, 'log', log=log)

                ### CAMBIAR DIR WRITE BACK
                wb_dir = cachedir + self.cachesize*cacheTag
                self.bus.write_back(wb_dir, data)
                ### CALL FN()

        if(hit):
            log = "$ WRITE HIT dir:{}\n".format(hex(dir))
            self.update_view(self.ID, 'log', log=log)
            self.hitRate += 1
        else:
            self.missRate += 1
        
        ### SAVE DATA IN CACHE 
        self.cache.write(cachedir,'modified',tag,data)       
        ### NOTIFY THE OTHERS CORES
        self.bus.notify_cores(dir, self.ID)
        ### UPDATE VIEW
        self.update_view(self.ID,'rate') 
        
    def notify_write(self,dir, id):
        #print("Checking WRITE from ID:{} dir:{} selfID:{}".format(id,dir,self.ID))

        if(id != self.ID):
            cachedir, tag = self.map_dir(dir)
            cacheTag = self.cache.get_tag(cachedir)
            validbit = self.cache.get_valid(cachedir)
 
            inCache = validbit != 'invalid' and tag == cacheTag
            #print("Checking in cache:{}, validbit:{}, cacheTag:{}, cachedir{}, dir{}, tag:{}".format(inCache, validbit, cacheTag, cachedir, self.bus.get_dir(), tag))

            if(inCache):
                self.cache.change_state(cachedir, 'invalid')
                log = "$ BUS WRITE MISS dir:{}\n".format(dir)
                self.update_view(self.ID, 'log', log=log)

    def notify_read(self, id, dir):
        inCache = False
        if(id != self.ID):
            cachedir, tag = self.map_dir(dir)
            cacheTag = self.cache.get_tag(cachedir)
            validbit = self.cache.get_valid(cachedir)
            inCache = validbit != 'invalid' and validbit != 'shared' and tag == cacheTag

            #print("Checking in cache:{}, validbit:{}, cacheTag:{}, cachedir{}, dir{}, tag:{}".format(inCache, validbit, cacheTag, cachedir, dir, tag))

            if(inCache):
                log = "$ BUS READ MISS dir:{}\n".format(hex(self.bus.get_dir()))
                self.update_view(self.ID, 'log', log=log)
                #print("putted data:",self.cache.read(cachedir))
                self.bus.set_data(self.cache.read(cachedir), self.ID)
                log = "$ SHARED FROM {} TO {}. dir:{} data:{}\n".format(self.ID, id, hex(self.bus.get_dir()), self.bus.get_data())
                self.update_view(self.ID, 'log', log=log)
                
                self.cache.change_state(cachedir, 'exclusive')

        return inCache
    
    