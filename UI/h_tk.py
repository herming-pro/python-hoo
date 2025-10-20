import h_tk_api
import ttk as ttk
import Tkinter as tk
import Language
from PIL import Image,ImageTk
import tk_style
import h_global

class main(h_tk_api.main):
    def __init__(self,oo):
        module_list = ["01panel"]
        self.oo = oo
        self.tk_root = tk.Tk() 
        self.Lan = Language.main("zn-TW")
        h_tk_api.main.__init__(self,tk,self.oo,self.tk_root)
        self.version = "v0.1.0"
        self.config_version = "v1.0.0"
        self.set_api_data(
            version = self.version,
            config_version = self.config_version,
            title = self.Lan.get("root_name") + " - " + self.version , 
            Language = [self.Lan,self.Language_chang]
            )
        self.set_windows_size(650,500)
        self.start()
        self.set_style()
        self.__import_main_list = []
        """
        標題畫面框
        """
        a="./ico/dev.ico"
        self.tk_root.iconbitmap(default=a)
        self.tk_root.title(self.title)
        """
        上方內容
        """

        """
        內容
        """
        lan = self.Language_chang
        self.note=self.Notebook(self.tk_root)
        self.note.place(x=15, relwidth=1, width=-30, y=50, relheight=1, height=-80)
        for i in module_list:
            #動態import
            __import_data_tmp = __import__(i)
            
            #動態繼承
            __tmp_list = [h_tk_api.main,self.Frame]
            __tmp_list += list(__import_data_tmp.main.__bases__)
            __import_data_tmp.main.__bases__  = tuple(__tmp_list)
            
            #加入到__import_main_list中
            self.__import_main_list.append(__import_data_tmp.main(tk,self.oo,self.tk_root))
            
            #初始化h_tk_api
            __import_data_tmp.main.__bases__[1].__init__(self.__import_main_list[-1],self.tk_root)
            
            #建立setloop
            self.oo.set_loop(self.__import_main_list[-1].ui_loop)
            
            #建立api資訊
            self.__import_main_list[-1].set_api_data(
                version = self.version,
                config_version = self.  config_version,
                title = self.Lan.get("name") + " - " + self.version , 
                Language = [self.Lan,lan]
                )
            #init
            self.__import_main_list[-1].init()
            
            #get_name
            __tmp_name =  self.__import_main_list[-1].get_name()           

            #note.add
            if str == type(__tmp_name):
                self.note.add(self.__import_main_list[-1],text=__tmp_name)
            else:
                self.note.add(self.__import_main_list[-1],text=__tmp_name.get())
                
            #set_ui
            self.__import_main_list[-1].set_ui()
            
        """
        底下
        """
        _text = "Herming@Insynerger - config version %s"%self.version
        self.Label(self.tk_root, text=_text ,style='gee.TLabel',anchor=tk.CENTER ).place(relx=0.02, relwidth=0.96, rely=1, y=-30, height=30)
    def Language_chang(self):
        self.set_api_data(title = self.Lan.get("root_name") + " - " + self.version)
        self.tk_root.title(self.title)
        for i ,j in enumerate(self.__import_main_list):
            j.Language_change() 
            __Text = j.get_name()
            if str != type(__Text):
                self.note.tab(i,text  = __Text.get())
    def set_style(self):
        tmp = tk_style.main()
        style = ttk.Style()
        current_theme =style.theme_use()
        style.theme_settings(current_theme, tmp.info())
        #style.theme_create("sty", parent="alt", settings=)
        #style.theme_use("sty")