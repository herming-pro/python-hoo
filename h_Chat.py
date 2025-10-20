import oo
import time
import sys

class main():
    def __init__(self,module_list=[],*args, **kwargs):
        self.auto_start(self.go)
        #初始化在此
        
        self.cmd_dict = {}
        self.task_dict = {}
        self.cmd_list = []
        self.run_list = 0
        self.MAX_JOBS = 10
        self._path_adder = oo.path_adder()
        self._path_adder.add_path("chat")
        
        
        try:
            for i in module_list:
                __import_data_tmp = __import__(i)
                tmp = __import_data_tmp.main(self.lock)
                self.cmd_dict.update({tmp.name():__import_data_tmp})
                self.Send('main','log',i)
        except:
            sys.excepthook(*sys.exc_info())
 
    def end(self):
        self.run_list -= 1
        self.start_task()
    def start_task(self):
        if self.cmd_list and self.run_list < self.MAX_JOBS:
            tmp = self.cmd_list.pop(0)
            JOBS    = tmp[0]
            TASK    = tmp[1]
            TASK_ID = tmp[2]
            if JOBS in self.cmd_dict.keys():
                #建立ID
                __ID = ""
                for i in xrange(self.MAX_JOBS):
                    if not("%03d"%i in self.task_dict.keys()):
                        __ID = "%03d"%i
                        break
                #try:
                self.task_dict.update({__ID:self.cmd_dict[JOBS].main(self.lock)})
                self.task_dict[__ID].init_chat(TASK,TASK_ID,__ID,self)
                self.task_dict[__ID].init()
                self.task_dict[__ID].start()
                self.run_list += 1
                self.Send(TASK,TASK_ID,__ID)
                #except Exception as a:
                #    self.log(str(a))
                    
    def go(self):
        '''
            init
            API指令
            add
            [<開啟的工作>,<回傳的目標>,<回傳的工作代碼>]
            *需再get 此工作代碼 task id
            set
            [<task id>,<value>]
            send
            [<task id>,<value>]
            del
            [<task id>]
        '''
        try:
            if not(self.full("add")):
                tmp = self.get_data("add")
                if type(tmp) == list and len(tmp) == 3:
                    self.cmd_list.append(tmp)
                    self.start_task()
            elif not(self.full("set")):
                self._API_SET(self.get_data("set"))
            elif not(self.full("send")):
                self._API_SEND(self.get_data("send"))
            elif not(self.full("del")):
                self._API_DEL( self.get_data("del") )
                
            else:
                self.pause() 
            
        except oo.time_out:
            self.log("time_out")
            self.pause() 
    def _API_SET(self,value):
        if type(value) == list and len(value) == 2:
            if self.task_dict.get(value[0]):
                self.task_dict[value[0]].set(value[1])
    def _API_SEND(self,value):
        if type(value) == list and len(value) == 2:
            if self.task_dict.get(value[0]):
                self.task_dict[value[0]].get(value[1])
    def _API_DEL(self,value):
        if type(value) == list and len(value) == 1:
            if self.task_dict.get(value[0]):
                self.task_dict[value[0]].stop()
                self.task_dict.pop(value[0])
                self.end()
    def stop(self):
        for i in self.task_dict.keys():
            self.task_dict[i].stop()
        oo.threading_object_class.stop(self)
class chat(oo.threading_object_class):
    def __init__(self,lock,*args, **kwargs):
        oo.threading_object_class.__init__(self,lock,*args, **kwargs)
        self.auto_start(self.loop)
    def init_chat(self,task,task_id,ID,oo):
        self.jobs = []
        self.task = task
        self.task_id = task_id
        self.oo = oo
        self.ID = ID
    def name(self):
        return "None"
    def init(self):pass
    def set(self,data):pass
    def stop(self):
        self.oo.end()
        oo.threading_object_class.stop(self)
    def send(self,data):
        self.oo.Send(self.task,self.task_id,data)
    def get(self,data):
        self.jobs.append(data)
        self.resume()
    def loop(self):pass