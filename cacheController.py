class controller:

    hitRate = 0
    missRate = 0
    thread_pause = None



    def __init__(self, _cache, _bus):
        self.cache = _cache
        self.cachesize = _cache.size
        self.bus = _bus
    
    def map_dir(self,dir):
        ### Find the tag and cache address
        ### Can work with different cache and memory size
        ### Can be replaced with a big if module
        cachedir = dir
        tag = 0
        while (dir > self.cachesize) :
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
            ### ASK BUS FOR THE DATA 
            ### CACHE DATA

        if(validbit == 'shared'):
            if(cacheTag != tag):
                miss = True
                ### ASK BUS FOR DATA
                ### CACHE DATA
        
        if(validbit == 'modified'):
            if(cacheTag != tag):
                miss = True
                ### STORE DATA AT MEMORY
                data = self.cache.read(cachedir)
                mem_dir = dir+self.cachesize if tag else dir                
                self.bus.write_back(mem_dir, data)
                ### ASK FOR NEW DATA
                self.bus.request_read(self.thread_pause, dir)
                ### CACHE DATA

        if(miss):
            self.missRate += 1
        else:
            self.hitRate += 1
        
        return self.cache.read(cachedir)


    def write(self, dir, data):
        cachedir,tag = self.map_dir(dir)
        ### CHECK IF DATA IS IN CACHE
        cacheTag = self.cache.get_tag(cachedir)
        validbit = self.cache.get_valid(cachedir)
        ### 
        hit = True
        if(validbit == 'modified'):
            if(cacheTag != tag):
                ### SAVE MISS
                hit = False 
                ### SAVE DATA IN MEMORY
                ### CALL FN()
        if(hit):
            self.hitRate += 1
        else:
            self.missRate += 1
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
    
    