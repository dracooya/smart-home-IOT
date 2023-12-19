class Event(object):
    def __init__(self):
        self.__listeners = []
        self.msg = ""
    
    @property
    def on(self):
        def wrapper(func):
            self.addListener(func)
            return func
        return wrapper
    
    def addListener(self,func):
        if func in self.__listeners: return
        self.__listeners.append(func)
    
    def removeListener(self,func):
        if func not in self.__listeners: return
        self.__listeners.remove(func)
    
    def trigger(self,args = None):
        if args is None:
            args = []
        for func in self.__listeners: func(*args)