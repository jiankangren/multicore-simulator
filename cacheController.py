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
            miss = True
         
        if(validbit == 'shared'):
            if(cacheTag != tag):
                miss = True
                
        if(validbit == 'modified'):
            if(cacheTag != tag):
                miss = True
                ### STORE DATA AT MEMORY
                data = self.cache.read(cachedir)
                ### WRITE BACK THE DATA
                self.bus.write_back(dir, data)
        
        ### IF THERE IS A MISS
        ### ASK BUS AND STORE IN CACHE
        
        if(miss):
            print("MISS READ")
            self.missRate += 1
            with self.thread_pause:
                ### ASK BUS FOR THE DATA 
                self.bus.request_read(self.thread_pause, dir) 
                ### SLEEPS the core
                self.core_state('SLEEP')
                self.thread_pause.wait()
                self.core_state ('AWAKE')
                
            ### CACHE DATA
            readed_data = self.bus.data
            self.cache.write(cachedir, 'shared', tag, readed_data)

        else:
            print("HIT READ")
            self.hitRate += 1
        
        self.update_view(self.ID,'rates')
        return self.cache.read(cachedir)


    def write(self, dir, data):
        cachedir,tag = self.map_dir(dir)
        ### CHECK IF DATA IS IN CACHE
        cacheTag = self.cache.get_tag(cachedir)
        validbit = self.cache.get_valid(cachedir)
        ### 
        # print("WRITE OPERATION")
        # print("CACHE DIR:{} TAG:{}".format(cachedir, tag))
        # print("CACHE TAG:{} VALID BIT:{}".format(cacheTag, validbit))
        
        hit = True
        if(validbit == 'modified'):
            if(cacheTag != tag):
                ### SAVE MISS
                hit = False 
                ### SAVE DATA IN MEMORY
                data = self.cache.read(cachedir)
                ### WRITE BACK THE DATA
                self.bus.write_back(dir, data)
                ### CALL FN()
        if(hit):
            print("HIT WRITE")
            self.hitRate += 1
        else:
            self.missRate += 1

        self.update_view(self.ID,'rate')        
        ### SAVE DATA IN CACHE 
        self.cache.write(cachedir,'modified',tag,data)
        ### NOTIFY THE OTHERS CORES
        self.bus.notify(dir)
        
        return

    def notify_write(self):
        cachedir, tag = self.map_dir(self.bus.dir)
        cacheTag = self.cache.get_tag(cachedir)
        validbit = self.cache.get_valid(cachedir)
        inCache = validbit != 'invalid' and tag == cacheTag
        if(inCache):
            self.cache.change_state(cachedir, 'invalid')

    def notify_read(self):
        cachedir, tag = self.map_dir(self.bus.dir)
        cacheTag = self.cache.get_tag(cachedir)
        validbit = self.cache.get_valid(cachedir)
        inCache = validbit != 'invalid' and tag == cacheTag
        if(inCache):
            self.bus.data = self.cache.read(cachedir)
        return inCache
    
    