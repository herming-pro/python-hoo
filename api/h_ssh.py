import paramiko
import socket
from scp import SCPClient
import time
import re
import sys

class time_out(Exception): pass
class error_not_find_data(Exception): pass    
class error_cmd_error(Exception): pass    

class time_cheak(object):
    #1S為單位 ，但支援小數點
    #int(datetime(tzinfo=timezone.utc).timestamp())
    def __init__(self):
        self._start_time = 0
        self._end_time = 0
    #設定time時間
    def set_time(self,time):self._end_time = time

    #開始計時
    def start(self):self._start_time = time.time()
        
    #判斷是否時間到(必須要先設定time，不然永遠都是到)
    def time_out(self):return True if time.time() - self._start_time >= self._end_time else False

    #判斷開始到現在經過多久
    def elapsed_time(self):return "%0.3f"%(time.time() - self._start_time)
    
class main(object):
    '''
    data = 
    ssh_set(**data)     設定連線資訊
        **data = *1 
        Exception data_error
    ssh_link(**data)    SSH連線
        **data = *1
        return True , False
    ssh_close()         關閉連線
        return True
    ssh_send(cmd ,endswith = ["$" , "#"])     發送SSH資訊
        cmd = 發送的指令，不用帶換行，會自動加入
        endswith = 結尾符號，預設為$或者為#，可以填入自己所想要的 (不用包含空白)
            except : "passwd :"<---可用於登入
            
        會將收到的所有資料存入ssh_buff(list)中，並且以\n切割
        
        return True , False
    ssh_get_error()     取得SSH錯誤
        如果上面函數有False，可以使用此函數取得錯誤訊息
    ssh_sftp_file(local_path , target_path = /tmp/ ,  mode = put)
        local_path  = 本地端的path，是str
        target_path = 目標端的path，預設放在/tmp/底下
        mode = put , get
            put = 將檔案從本地傳輸到對方
            get = 將檔案從對方傳輸至本地
    -------------
        *1 data =連線資訊，會記錄在_data中
            |name     |  預設值       |   說明
            |-------------------------------------
            |ip       |  無預設       |   目標地址
            |port     |  0            |   目標序列埠
            |username |  無預設       |   使用者
            |password |  無預設       |   密碼
            |root     |  False        |   是否要切換root
            |timeout  |  60           |   連線超時
    '''
    def __init__(self):
        paramiko.util.log_to_file("filename.log")
        self._ssh_client = paramiko.SSHClient()
        self._ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self._link = False
        self._data = { "ip":"",
                        "port":0,
                        "username":"",
                        "password":"",
                        "root_password":False,
                        "timeout":60}
        self.__reset_buff()
        self._time = time_cheak()
    def _log(self,data):
        if True:
            print str(data)
    def __reset_buff(self):
        self.ssh_error = ""
        self.ssh_buff = []
    def __send(self , cmd = "" ,t = 0.5) :
        try:
            #print cmd
            self._ssh.send("%s\n"%cmd)
            time.sleep(t)
        except Exception as a:
            sys.excephook(*sys.exc_info())
            self.ssh_error = str(a)
            return False
        return True
    def __read(self,cmd):
        _tmp = ""
        try:
            _tmp = self._ssh.recv(9999)
        except socket.timeout:
            pass
        _tmp = ''.join(_tmp.split('%s\r\n'%cmd, 1))
        uncolored = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        return uncolored.sub('', _tmp)
    def __ch_root(self,cmd):
        self._time.set_time(3)
        self.ssh_send(cmd,[],1)
        if self.ssh_buff[-1].endswith(":"):
            if self.ssh_send(self._data.get("root_password",""),["#"]):#成功
                return True
            else:
                self.ssh_error = "root passwd error"
                return False
        elif self.ssh_buff[-1].endswith("#"):#成功
            return True
        elif self.ssh_buff[-1].endswith("$"):
            
            return False
    def data_chean(self,tmp_res):
        tmp = tmp_res.split("\n")
        tmp_list = []
        for i in tmp :
            tmp_list.append(i.rstrip())
        return tmp_list
    def ssh_set(self,**kw):
        for i in kw.keys():
            if not(i in self._data.keys()):
                self.ssh_error = "%s not in conf."%i
                raise error_not_find_data()
            elif kw[i] == "":
                del kw[i]
        self._data.update(kw)
        return True
    def ssh_link(self,**data):
            self.ssh_set(**data)
        #try:
            self._ssh_client.connect(   self._data.get("ip",""),
                                        int(self._data.get("port",0)),
                                        self._data.get("username",""),
                                        self._data.get("password",""))
            self._ssh = self._ssh_client.invoke_shell()
            
            self._sftp=SCPClient(self._ssh_client.get_transport(),socket_timeout = 60)
            
            self._ssh.settimeout(3)
           
            self.__reset_buff()
            self.ssh_error == u"time out"  
            resp = ""
            tmp = ""
            self._time.set_time(3)
            _time_out = time_cheak()
            _time_out.set_time(self._data.get("timeout",60))
            _time_out.start()
            
            while not _time_out.time_out():
                resp = self.ssh_send("",endswith = ['#'])
                self._time.set_time(self._data.get("timeout",60))
                self._link = True
                if self.ssh_buff[-1] == "":
                    return True
                elif  self.ssh_buff[-1].endswith('$'):
                    if self._data.get("root_password",False):
                        
                        if self.__ch_root("su"):
                            return True
                        else:
                            if self.ssh_error == "root passwd error":
                                return False
                            else:
                                if self.__ch_root("sudo -i"):
                                   return True
                                else:
                                    self.ssh_error == "can't cheng root"
                                    return False
                    else:
                        return True
                      
            self.ssh_error == u"time out"   
            return False
        #except Exception as e:
        #    self.ssh_error = u"%s"%(e.__str__().decode('big5'))
        #    return False
    def ssh_send(self,command , endswith = ['#',"$"],t = 0.1):
        self.__reset_buff()
        tmp_res = ""
        
        if not( self.__send("%s\n"%command,t)):
            self.ssh_error = "send error"
            return False
        self._time.start()
        while not (self._time.time_out()):
            tmp = self.__read(command) 
            tmp_res+= tmp
            for i in endswith:
                if tmp.rstrip().endswith(i):
                    self.ssh_buff = self.data_chean(tmp_res)
                    for j in xrange(len(self.ssh_buff),0,-1):

                        if not (self.ssh_buff[j-1].endswith(i)):
                            self.ssh_buff = self.ssh_buff[:j]
                            return True
                
        self.ssh_buff = self.data_chean(tmp_res)
        
        self.ssh_error = "time out"
        return False
    def ssh_close(self):
        self._ssh.close()
        return True
    def ssh_get_error(self):
        return self.ssh_error
    def ssh_sftp_file(self,local_path , server_path = "/tmp/",mode  = "put") :#傳檔
        if mode == "get":
            self._sftp.get(server_path, local_path)
        elif mode == "put":
            self._sftp.put(local_path, server_path)
        else:
            raise error_cmd_error()
        return True
    def ssh_exitCode(self):
        if not self.ssh_send('echo $?'):
            return False
        else:
            return self.ssh_buff
    def ls(self,*args,**kw):
        pass
    def cd(self,*args,**kw):
        pass
    def printer(self,text=False):
        if text==True:
            return '\n'.join(self.ssh_buff)
        elif text==False:
            print '-'*60
            print '\n'.join(self.ssh_buff)
            
if __name__ == '__main__':
    ssh = main()
    ssh.ssh_set(ip="192.168.0.100",
                port=2022,
                username="yourname",
                password="userpawd",
                root_password="pawd")
    if ssh.ssh_link():
        ssh.printer()
        ssh.ssh_send("test -f /home")
        ssh.ssh_send("echo $?")
        ssh.printer()
    print ssh.ssh_get_error()

