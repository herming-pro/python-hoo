import h_open
"""
 _    _              ________                 
| |__| |.-----.----.|        | - .-----.-----.
|  __  ||  -__|   _||  |  |  |.-.|     |  _  |
|_|  |_||_____|__|  |__|__|__||_||__|__|__   |
                                        __|  |
 ┌─────────────────────────────────────|_____|
 │2022 / 05 / 03  v 1 . 0 . 0               │
 │modbus scanning                           │
 └──────────────────────────────────────────┘
"""
class main():
    '''
    JOBS Data 參數
    ["nb" , "ip" , "path" , "username" , "passwd" , "report" ]
    回傳
    目前狀態回報
    status { "nb" : <第幾個裝置> , "info" : <目前狀態>}
    結果回報
    失敗
    info   { "nb" : <第幾個裝置> , "info" : <結果 True / False> , "data" : {"None" : <保留>}}
    成功
    info   { "nb" : <第幾個裝置> , "info" : <結果 True / False> , "data" : {
                "mac"       : <MAC> , 
                "ver"       : <版本> , 
                "path"      : <設定的路徑>, 
                "username"  : <設定的使用者名稱>, 
                "passwd"    : <設定的密碼>, 
                "report"    : <設定的回報時間>
                }
           }
    
    ##send 規則：
    self.oo.Send("JOBS","jobs",[ 工作 , 你的名稱 , 參數(list) ])
    
    ("modbus2UI", self.channel) 分別為與modbus做(接收,傳送)時所用的頻道
    ex:
    self.oo.th_get_data('modbus2UI', timeout = 3)
    self.oo.get_data('modbus2UI')
    self.oo.Send('CHAT', 'send', [self.channel, (符合API形式的資料)])
    
    self.currentID = 當前選定設備的流水號 => self.idlist[self.currentID]
    
    self.taglist = 存放當前使用的tag('00'~'99')
    self.local_data = 蒐集從get_data拿到不符合tag的資料 格式:{tag:data}
    '''
####################主程式####################
    def init(self):
        self.name = "tools"
        # 變數初始化
        self.slavelist   = []
        self.slavestring = []
        self.buttonList  = []
        self.buttonCongig = {"relx":0.5 , "x" : -40 ,"rely":0.5, "y" : -15 ,"width":80, "height":30}
        self.buttonNone   = {"relx":1 ,"rely":1 , "width":0, "height":0}
        self.titel_size  = [0.18 , 0.21 , 0.43 , 0.18]
        self.framlen = 40
        self.flag = False
        self.sendsetting = []
        self.allslave = []
    def get_name(self):
        return "測試"
    def button_check(self,data):
        self.oo.Send("main","log",data)
        s = data.split("_")
        if(s[0] == "B02"):
            if(s[1] == "00"):
                #新增
                #["nb" , "path" , "username" , "passwd" , "report" ]
                req = [
                    len(self.slavelist) ,
                    "192.168.0.101",
                    "test/path",
                    "herming",
                    "0dme" ,
                    60
                ]
                self.oo.Send("JOBS" , "jobs" , [ "updata" , "UI" , req])
                self.add_slave(["192.168.0.1" , "-" , "-" , "等待中"])
                
            elif(s[1] == "01"):
                for i in self.buttonList :   
                    i.place(**self.buttonNone )
                for i in self.slavestring :
                    i[3].set("發呆中")
            elif(s[1] == "02"):
                #匯出
                for i in self.slavestring :
                    i[3].set("")
                for i in self.buttonList :   
                    i.place(**self.buttonCongig )
            elif(s[1] == "03"):
                self.VSF.clean()
                self.slavelist   = []
                self.slavestring = []
                self.buttonList  = []
        if(s[0] == "B03"): 
            nb = int(s[2])
            self.buttonList[nb].place(**self.buttonNone )
            req = [
                nb , 
                "192.168.20.213",
                "test/path",
                "herming",
                "0dme" ,
                60
            ]
            self.oo.Send("JOBS" , "jobs" , [ "updata" , "UI" , req])
            self.slavestring[nb][3].set("等待重試")
                
    def ui_loop(self):
        if not(self.oo.full(self.name)):
            tmp = self.oo.get_data(self.name)
            self.oo.log('get name from %s :%s'%(self.name,tmp))
        if not(self.oo.full("status")):
            data = self.oo.get_data("status")
            self.oo.log(data)
            if(data.get("nb" , 9999) < len(self.slavelist)):
                nb = data["nb"]
                self.slavestring[nb][3].set(data.get("info" , ""))
        if not(self.oo.full("info")):
            data = self.oo.get_data("info")
            self.oo.log(data)
            if(data.get("nb" , 9999) < len(self.slavelist)):
                
                nb = data["nb"]
                if(not data.get("info" , False)):
                    #失敗的話
                    self.buttonList[nb].place(**self.buttonCongig )
                    self.slavestring[nb][3].set(data.get("info" , ""))
                    
                else:
                    #成功的話
                    #將data存起來
                    req = data.get("data" , {})
                    self.oo.log("--"*10)
                    self.oo.log(req)
                    self.slavestring[nb][1].set(req.get("mac" , ""))
                    self.slavestring[nb][2].set(req.get("ver" , ""))
                    self.slavestring[nb][3].set("成功")
            
    def set_ui(self,):
        #左側
        LI = self.Frame(self , relief = "sunken")
        LI.place( relx = 0 , rely = 0.05 ,relwidth=0.2 , relheight = 0.9)
        
        #新增
        self.Button(LI , tag = "B02_00" , text = "新增").place(relx=0.5,x = -50, width=100 , rely=0.1, y =-15 , height=30)
        self.Button(LI , tag = "B02_01" , text = "設定").place(relx=0.5,x = -50, width=100 , rely=0.3, y =-15 , height=30)
        self.Button(LI , tag = "B02_02" , text = "匯出").place(relx=0.5,x = -50, width=100 , rely=0.5, y =-15 , height=30)
        self.Button(LI , tag = "B02_03" , text = "清空").place(relx=0.5,x = -50, width=100 , rely=0.7, y =-15 , height=30)

        #建立元件
        self.VSF = self.VerticalScrolledFrame(self)
        self.VSF.place( relx = 0.20 , rely = 0.05 ,relwidth=0.8 , relheight = 0.9)
        ti = self.VSF.add_Title()
        flag = 0
        name = ["IP" , "MAC" , "版本" , "狀態"]
        for i , j  in enumerate(name):
            self.Label(ti , text = j , relief = "sunken").place(relx=flag ,rely=0,relwidth=self.titel_size[i], relheight=1)
            flag += self.titel_size[i]

    def add_slave(self, data):
        nb = len(self.slavelist)
        self.slavelist.append(self.VSF.add_Frame(self.framlen))
        
        self.slavestring.append([self.StringVar() , self.StringVar() , self.StringVar() , self.StringVar()])
        flag = 0
        for i , j in enumerate(data):
            self.slavestring[-1][i].set(j)
            f = self.Frame(self.slavelist[-1] , relief = "sunken")
            f.place(relx=flag ,rely=0,relwidth=self.titel_size[i], relheight=1)
            self.Label(f , textvariable = self.slavestring[-1][i] , relief = "sunken").place(relx=0 ,rely=0,relwidth=1, relheight=1)
            flag += self.titel_size[i]
        self.buttonList.append(self.Button(f , tag = "B03_00_%05d"%nb , text = "重試"))
    def del_tabel(self , nb):
        print(self.slavelist)
        self.VSF.delete_Frame(self.slavelist[nb])
        self.slavelist.pop(nb)  
        self.slavestring.pop(nb)   