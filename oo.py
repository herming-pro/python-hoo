"""
V0.5
傳送變數資料方式：
self.Send(direction,name,data)
direction = 目標
name = 變數名稱
data = 物件

傳送 停止、結束執行緒：
    self.Send(direction,status)
    status = stop(停止),start(啟動),pause(暫停)
    
接收變數：
_name_ = self.get_data(name,cmd = data)
_name_ = 變數
name = 變數名稱
**如果該name沒有值，會回傳None
cmd = 要接收什麼
    data = 資料
    all = {"who" : 誰傳過來的 , "data" : 資料}
    who = 誰傳過來的
**預設為data
arraymode = 資料結構 
    Queue|| Stack
**預設為Queue

listenmode = 取得模式
    get = 只取得不刪除
    pop = 取得後刪除
**預設為pop


結束執行緒：
self.exit()

多執行緒操作：
self.pause()
使單一多執行緒暫停

self.resume()
使單一多執行緒繼續

self.stop()
使單一多執行緒停止

self.exit()
使全部多執行緒停止


"""
SEND_NB = 0
TAKE_NB = 1
NAME_NB = 2
DATA_NB = 3


#計時功能
import time
class time_out(Exception): pass
class time_cheak(object):
    #s為單位，但支援小數點
    def __init__(self):
        self._start_time = 0.0
        self._end_time = 0.0
    #設定time時間
    def set_time(self,time):self._end_time = float(time)

    #開始計時
    def start(self):self._start_time = time.time()
        
    #判斷是否時間到(必須要先設定time，不然永遠都是到)
    def time_out(self):return True if time.time() - self._start_time >= self._end_time else False

    #判斷開始到現在經過多久
    def elapsed_time(self):return time.time() - self._start_time
#執行續與進程續相同的部分
class object_class(object):
    def __init__(self , running , flag):
        self.running = running
        self.flag = flag        
    def auto_start(self,loop_func = False,fist_func = False , end_func   = False):
        self._fist_func = fist_func
        self._loop_func = loop_func 
        self._end_func = end_func 
    def th_get_data(self,name,cmd = "data",timeout = 36400):
        now_time = int(round(time.time() ))
        while self.running.isSet():
            if not(self.full(name)):
                tmp = self.get_data(name,cmd)
                return tmp
            if int(round(time.time() )) - now_time >= timeout:
                return None   
            self.flag.wait(timeout)   
        raise time_out()   
    def run_info(self):
        if self._fist_func:
            self._fist_func()
        if self._loop_func:
            while self.running.isSet():
                self.flag.wait()
                self._loop_func()
        if self._end_func:
            self._end_func()
    def pause(self):#暫停
        self.flag.clear() 
    def resume(self):#開始
        self.flag.set()
    def stop(self):#結束
        self.running.clear()
        self.flag.set()
#多進程緒
import multiprocessing
class multiprocessing_object_class(multiprocessing.Process , object_class):
    def __init__(self,lock,*args, **kwargs):
        #super(multiprocessing_object_class, self).__init__(*args, **kwargs)
        multiprocessing.Process.__init__(self)
        self.flag = multiprocessing.Event()
        self.flag.set()
        self.running = multiprocessing.Event()
        self.running.set()
        self.th_fist_func  = False
        self.th_loop_func  = False
        self.th_end_func   = False
        object_class.__init__(self,self.running, self.flag)
    def run(self):
        self.run_info()
      
#多執行緒
import threading
class threading_object_class(threading.Thread , object_class):
    def __init__(self,lock,*args, **kwargs):
        super(threading_object_class, self).__init__(*args, **kwargs)
        threading.Thread.__init__(self)
        self.flag = threading.Event()
        self.flag.set()
        self.running = threading.Event()
        self.running.set()
        self.th_fist_func  = False
        self.th_loop_func  = False
        self.th_end_func   = False
        self.lock = lock
        object_class.__init__(self,self.running, self.flag)
    def run(self):
        self.run_info()
#path 管理
import os
import sys

class path_adder():
    def __init__(self):
        self.data_path=os.path.dirname(sys.argv[0])
        os.path.dirname(sys.executable)
        if self.data_path == "":
            self.data_path='.'
    def add_path(self,name):
        try:
            sys.path.append("%s/%s"%(self.data_path,name))
            return True
        except:
            return False
#callback 主main
'''
使用方法

add_threading 
    新增一個新的多執行續，該多執行續需繼承 threading_object_class
    
    參數：
        import_obj      : 需載入的套件
        name            : 該多執行續的名稱   
        *args,**kwargs  : 會代入 import class 的剩餘資訊
        
        套件初始化內容
        name            : 該多執行續的名稱 ， 如果有繼承 callback_object_class 代入即可
        __callback      : callable func ， 如果有繼承 callback_object_class 代入即可
        lock            : 該多執行續的鎖，可以鎖住全部的 class
        *args,**kwargs  : 代入 import class 的剩餘資訊
        
start
    啟動多執行續，需要先經過新增
    
    參數：
        
    

'''

import imp
#callback 執行緒
class callback_object_class():
    def __init__(self,function_name, callback):
        self.sendcount = 100
        self.callback = callback
        self.my_direction = function_name
        self.variable_dict = {"exit":{"data":False,"who":"main"}}
    def h_import(self, path , name):
        try:
            __import_data_tmp = imp.load_source('', path)
            _bases_list = [callback_object_class]
            _bases_list += list(__import_data_tmp.main.__bases__)
            __import_data_tmp.main.__bases__  = tuple(_bases_list)
            tmp = __import_data_tmp.main(name,self.callback)
            return True , tmp
        except:
            sys.excepthook(*sys.exc_info())
            return False , None
    def Send(self,direction,name,data=""):# 發送訊息 (給誰,變數名稱(動作/指令),資料(可以空的))
        return self.callback(self.my_direction , direction , name ,data)
    def log(self,data):
        self.Send("main" , "log" , data)
    def set(self,data):
        if(len(data) < 4):
            return
        name = data[NAME_NB]
        # self.Send('main','log','set,%s,%s'%(who,name))
        if not(name in self.variable_dict.keys()):
            self.variable_dict.update({name:[]})
        if(len(self.variable_dict[name]) >= self.sendcount):
            self.variable_dict[name].pop(0)
        self.variable_dict[name].append({"data":data[DATA_NB],"who":data[SEND_NB]})
    def full(self,name):#如果空的，回True
        data = self.variable_dict.get(name,[])
        if len(data) > 0:
            return False
        else:
            return True
    def get_data(self,name,cmd = "data" , arraymode = 'Queue' , listenmode = 'pop'):#取得變數
        # arraymode  = Queue || Stack
        # listenmode = get   || pop
        
        try:
            if(arraymode == 'Queue'):
                nb = 0
            elif(arraymode == 'Stack'):
                nb = -1
            else:
                nb = 0
            if(listenmode == 'get'):
                tmp = self.variable_dict.get(name,[None])[nb]
            elif(listenmode == 'pop'):
                tmp = self.variable_dict.get(name,[None]).pop(nb)
            else:
                tmp = None
            
        except  IndexError as a :
            tmp = None
        if(tmp == None):
            return None
        return{
            "data":tmp.get("data",""),
            "all":tmp,
            "who":tmp.get("who",""),
        }.get(cmd,None)
    def exit(self):
        self.Send("","exit")
class callback_object_obj(threading_object_class , callback_object_class):
    def __init__(self ,function_name,callback,lock  , main ,*args, **kwargs ):
        threading_object_class.__init__(self,lock)
        callback_object_class.__init__(self,function_name,callback)
        main.__init__(self  , *args, **kwargs)
        self.function_name = function_name
class callback_object_main():
    def __init__(self):
        self.flag = threading.Event()
        self.flag.set()
        self.showName = True
        self.__THREADING_DICT = {}
        self.__CALLBACK_DATA = []
        self.__CALLBACK_MAX_LEN = 100
        self.__debug_level = 0
        self.__new_read = False
        self.lock = threading.Lock()
    def add_threading(self,import_obj,name , *args,**kwargs):
        if name in self.__THREADING_DICT.keys():
            return False
        try:
            self.__main_log(0,"[add_threading] >>",import_obj.__module__)
            #import_obj
            tmp = callback_object_obj
            tmp = type( tmp.__name__, (import_obj,) + tmp.__bases__ ,dict(tmp.__dict__))
            
            self.__THREADING_DICT.update({name:tmp(name, self.__callback , self.lock , import_obj ,*args,**kwargs)})
        except Exception as a :
            self.__main_log(0,"[add_threading Exception] >>","%s\t%s"%(a,name))
            return False
        return True
    def start(self,name):
        if name =="all":
            for i in self.__THREADING_DICT.keys():
                self.__THREADING_DICT[i].start()
        elif name in self.__THREADING_DICT.keys():
            self.__THREADING_DICT[name].start()
        else:
            return False
        return True
    def del_threading(self,name):
        if not(name in self.__THREADING_DICT.values()):
            return False
        self.__THREADING_DICT[name].stop()
        del self.__THREADING_DICT[name]
        return True
    def stop(self):
        self.flag.set()
        for i in self.__THREADING_DICT.values():
            self.__main_log(1,"[stop]>>",i)
            i.stop()
    def __debug_log(self,level,excel,log):
        if self.__debug_level >= level:
            print(excel)
            sys.excepthook(*log)
            print('</debug>')
    def __main_log(self,level,*log):
        if self.__debug_level >= level:
            tmp = ""
            for i in log:
                try:
                    tmp +="%s"%str(i)
                except:
                    tmp +="%s"%i
            print(tmp)
    def set_path(self,direction="",data=""):
        if direction != "":
            FIST_PH = direction
        if data != "":
            DATA_PH = data
        return True    
    def read(self):
        self.flag.wait(1)
        if len(self.__CALLBACK_DATA) > 0:
            CALLBACK_TMP = self.__CALLBACK_DATA.pop(0)
            return self.__sendDAta(CALLBACK_TMP)
        else:
            self.flag.clear() 
        return ""
    def __sendDAta(self , CALLBACK_TMP):
        if(len(CALLBACK_TMP) < 4):
            return False
        #SEND_NB = 0
        #TAKE_NB = 1
        #NAME_NB = 2
        #DATA_NB = 3
        FOR_HOW =  CALLBACK_TMP[TAKE_NB]
        DO_WHAT =  CALLBACK_TMP[NAME_NB]
        data    =  CALLBACK_TMP[DATA_NB]
        name    =  CALLBACK_TMP[SEND_NB]
        if FOR_HOW in self.__THREADING_DICT.keys():#stop(停止),start(啟動),pause(暫停)
            self.__main_log(1,"[read CALLBACK]>>",CALLBACK_TMP)
            if DO_WHAT == "stop":   
                self.__THREADING_DICT.get(FOR_HOW).stop()
            elif DO_WHAT == "start":
                self.__THREADING_DICT.get(FOR_HOW).resume()
            elif DO_WHAT == "pause":
                self.__THREADING_DICT.get(FOR_HOW).pause()
            else:
                self.__THREADING_DICT.get(FOR_HOW).set(CALLBACK_TMP)
                self.__THREADING_DICT.get(FOR_HOW).resume()
        elif  FOR_HOW == "main"  :
            if DO_WHAT == "log":  
                if(self.showName):
                    self.__main_log(0,"[%s]>>"%name,data)
                else :
                    self.__main_log(0,data)
            elif DO_WHAT == "debug":  
                self.__debug_log(0,"<debug>\n[%s]"%name,data)
        if "exit" in DO_WHAT:
            self.stop()
            exit()
        return True
    def run(self):
        try :
            while self.flag:
                self.read()
        except KeyboardInterrupt:
            self.stop()
        except Exception as a:
            print(a)
            main.stop()
    def new_read(self , message):
        flag = self.__sendDAta(message)
        self.flag.clear() 
        return flag
    def set_debuglevel(self,level):
        self.__debug_level = int(level)
    def set_new_read(self,flag):
        #2023 12 05 by herming , new read ,callback 結束直接去read，減少延遲問題以及空間問題
        self.__new_read = flag
    def __callback(self,*data):
        self.__main_log(2,"[callback fun]>>",data)
        if self.__new_read :
            return self.new_read(data)
        else:
            if len(self.__CALLBACK_DATA) >= self.__CALLBACK_MAX_LEN :
                self.__CALLBACK_DATA.pop(0)
            self.__CALLBACK_DATA.append(data)
            self.flag.set()
        return True
        #else:
        #    return False 
