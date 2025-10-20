import oo
import time
import sys

class main():
    def __init__(self, module_list = []):
        self.auto_start(self.go)
        #初始化在此
        
        self.cmd_dict = {}
        self.cmd_list = []
        self.run_list = 0
        self.MAX_JOBS = 10
        
        self._path_adder = oo.path_adder()
        self._path_adder.add_path("jobs")
        try:
            for i in module_list:
                __import_data_tmp = __import__(i)
                __import_data_tmp = type( __import_data_tmp.main.__name__,(jobs,) + __import_data_tmp.main.__bases__,dict(__import_data_tmp.main.__dict__))
                self.cmd_dict.update({i.split("_",1)[1]:__import_data_tmp})
                
        except:
            self.Send('main','debug',sys.exc_info())
    
    def end(self , fn,name):
        self.log("[%s][%s] jobs end"%(fn , name ))
        self.run_list -= 1
        self.start_task()
    def start_task(self):
        if self.cmd_list and self.run_list < self.MAX_JOBS:
            tmp = self.cmd_list.pop(0)
            if tmp[0] in self.cmd_dict.keys():
                try:
                    tmp_ = self.cmd_dict[tmp[0]](tmp[0],self.callback,self.lock , self.end , tmp[1])
                    tmp_.init(tmp[2])
                    tmp_.start()
                    self.run_list += 1
                except Exception:
                    self.Send('main','debug',sys.exc_info())
                    
    def go(self):
        try:
            s = self.th_get_data("jobs",timeout = 3)
            self.Send('main','log',s)
            if s==None:
                self.log("time_out")
                self.pause()
            elif len(s) == 3 and type(s) == list:
                self.cmd_list.append(s)
                self.start_task()
                time.sleep(1)
        except:
            self.Send('main','debug',sys.exc_info())
class jobs(oo.threading_object_class , oo.callback_object_class):
    def __init__(self,function_name,callback,lock, end , tag ,*args, **kwargs):
        oo.threading_object_class.__init__(self,lock,*args, **kwargs)
        oo.callback_object_class.__init__(self,function_name,callback)
        self.function_name = function_name
        self.__end = end
        self._tag = tag
    def init(self,data):
        self.dataList = data
    def run(self):
        try:
            self.do()
        except:
            self.Send('main','debug',sys.exc_info())
        self.end_jobs()
    def end_jobs(self):
        self.__end(self.function_name , self.name)
    def send(self , kw , data):
        self.Send(self._tag , kw , data)
    def do(self):pass
    