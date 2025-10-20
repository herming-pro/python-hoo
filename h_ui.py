import oo
import h_tk
import time
class main():
    def __init__(self,*args, **kwargs):
        #初始化在此
        self._time = oo.time_cheak()
        self.loop_list = []
        self.FPS = 20.0
    def set_loop(self,fun)  :
        self.loop_list.append(fun)
    def run(self):
        self.__h_tk = h_tk.main(self)
        while self.running.isSet():
            self.flag.wait()
            self._time.start()
            for i in self.loop_list:
                try:
                        i()
                except Exception as a:
                    self.Send("main","log",a)
            tmp_time =self._time.elapsed_time() 
            if tmp_time < 1/self.FPS:
                time.sleep(1/self.FPS - tmp_time )
            try:
                self.__h_tk.update()
            except Exception as a:
                self.Send("main","log",a)
                self.exit()
            
        """
        try:
            s = self.th_get_data("log",timeout = 10)
            self.Send("main","log",s)
        except oo.time_out:
            self.Send("main","log","time_out")
            self.pause() 
        """ 