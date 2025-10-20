import ftplib
from ftplib import error_perm
import os  
import sys

# 修正FTPserver回傳PASV IP位置不能使用
def makepasv(self):
    if self.af == 2:
        host_2, port = ftplib.parse227(self.sendcmd('PASV'))
    else:
        host_2, port = ftplib.parse229(self.sendcmd('EPSV'), self.sock.getpeername())
    return self.host, port
setattr(ftplib.FTP,'makepasv',makepasv)

class FileStructure():
    def __init__(self,name=''):
        self.name = name
        self.sub = {}
        self.type = None
    def setType(self,type,path=''):
        if path:
            file = self.getFile(path)
            if file:
                file.type = type
        else:
            self.type = type
    def add(self,path):
        if path:
            if '/' in path:
                name,sub = path.split('/',1)
                if name not in self.sub:
                    self.sub[name] = FileStructure(name)
                if sub:
                    self.sub[name].setType('d')
                    self.sub[name].add(sub)
            elif path not in self.sub:
                self.sub[path] = FileStructure(path)
    def exists(self,path):
        if path:
            if '/' in path:
                name,sub = path.split('/',1)
                if name not in self.sub:
                    return False
                else:
                    return self.sub[name].exists(sub)
            elif path in self.sub:
                return True
            else:
                return False
        elif self.type=='d':
            return True
        else:
            return False
    def getType(self,path):
        if path:
            if '/' in path:
                name,sub = path.split('/',1)
                if name not in self.sub:
                    return False
                else:
                    return self.sub[name].getType(sub)
            elif path in self.sub:
                return self.sub[path].type
            else:
                return False
        else:
            return self.type
    def getFile(self,path):
        if path:
            if '/' in path:
                name,sub = path.split('/',1)
                if name not in self.sub:
                    return False
                else:
                    return self.sub[name].getFile(sub)
            elif path in self.sub:
                return self.sub[path]
            else:
                return False
        else:
            return self
    def clear(self,):
        self.sub.clear()
    def __str__(self):
        return self.printer()[:-1]
    def printer(self,tab=0):
        TAB = ' '*4
        text = TAB*tab+self.name
        if self.type=='d':
            text+='/\n'
        else:
            text+=' '+str(self.type)+'\n'
        for name in self.sub:
            text += self.sub[name].printer(tab+1)
        return text
        
class Root(FileStructure):
    def __init__(self,name=''):
        FileStructure.__init__(self,name)
        self.type = 'd'
    def setType(self,type='d',path=None):
        if path!='/':
            file = self.getFile(path)
            if file:
                file.setType(type)
    def add(self,path):
        path = self.canonical(path)
        if not path:
            return False
        FileStructure.add(self,path[1:])
    def exists(self,path):
        path = self.canonical(path)
        if not path:
            return False
        else:
            return FileStructure.exists(self,path[1:])
    def getType(self,path):
        path = self.canonical(path)
        if not path:
            return False
        else:
            return FileStructure.getType(self,path[1:])
    def getFile(self,path):
        path = self.canonical(path)
        if not path:
            return False
        else:
            return FileStructure.getFile(self,path[1:])
    def canonical(self,path):
        if not path or path[0]!='/':
            return ''
        resPath = ''
        for dirname in path.split('/'):
            if not dirname or dirname=='.':
                continue
            elif dirname=='..':
                resPath = resPath.rsplit('/',1)[0]
            else:
                resPath += '/'+dirname
        return resPath if resPath else '/'

class main():
    def __init__(self):
        self.ftp = ftplib.FTP()
        self.ftp.set_debuglevel(0) #打開調適級別0，不顯示詳細訊息
        self.uploadCount = 0
        self.downloadCount = 0
        self.deleteCount = 0
        
        self.root = Root()
        
    def login(self,host,port,user,passwd,timeout=3):
        self.user = user
        self.passwd = passwd
        try:
            #連線的ftp sever和埠
            self.ftp.connect(
                host=host,
                port=port,
                timeout=timeout,
            )
            #連線的使用者名稱，密碼
            self.ftp.login(
                user=user,
                passwd=passwd,
            )
            return True
        except:
            sys.excepthook(*sys.exc_info())
            return False
    def dir(self,path=''):
        try:
            callback = []
            self.ftp.dir(path,callback.append)
            return callback
        except:
            self.ftp.dir(path,callback.append)
            return callback
    def ls(self,path='',exc=True):
        try:
            path = self.canonical(path)
            res = {}
            for line in self.dir(path):
                type,filename = line[0],line[56:]
                if type not in res:
                    res[type] = set()
                res[type].add(filename)
            if res:
                self.root.add(path)
                self.root.setType('d',path)
                dir = self.root.getFile(path)
                for type,names in res.items():
                    for name in names:
                        dir.add(name)
                        dir.setType(type,name)
            return res
        except error_perm as ex:
            if ex:
                raise ex
            else:
                sys.excepthook(*sys.exc_info())
                return {}
    def exists(self,path):
        path = self.canonical(path)
        if self.root.exists(path):
            return True
        else:
            dir,name = path.rsplit('/',1)
            self.ls(dir)
            return self.root.exists(path)
    def type(self,path):
        path = self.canonical(path)
        type = self.root.getType(path)
        if type:
            return type
        else:
            dir,name = path.rsplit('/',1)
            self.ls(dir)
            return self.root.exists(path)
    def cd(self,path):
        try:
            self.ftp.cwd(path) #設置FTP當前操作路徑
            return True
        except error_perm:
            sys.excepthook(*sys.exc_info())
            return False
    def pwd(self):
        return self.ftp.pwd()
    def mkdir(self,dirname):
        try:
            if not(dirname in self.ls().get('d',[])):
                self.ftp.mkd(dirname)
            return True
        except:
            return False
    def canonical(self, remotePath):
        if remotePath[0]=='/':
            dirlist = remotePath.split('/')
        else:
            dirlist = self.pwd().split('/')+remotePath.split('/')
        resPath = ''
        for dirname in dirlist:
            if not dirname or dirname=='.':
                continue
            elif dirname=='..':
                resPath = resPath.rsplit('/',1)[0]
            else:
                resPath += '/'+dirname
        return resPath if resPath else '/'
    def uploadFile(self,localPath,remoteDir='',remoteName='',check=True):
        if check and not os.path.isfile(localPath):
            return False
        if not remoteName:
            remoteName = os.path.abspath(localPath).rsplit('\\',1)[-1]
            
        if remoteDir:
            if not check or self.exists(remoteDir):
                remoteFile = self.canonical(remoteDir+'/'+remoteName)
            else:
                return False
        else:
            remoteFile = remoteName
            
        print remoteFile
        if remoteName not in self.ls(remoteDir)['-'] or self.ftp.size(remoteFile) != os.path.getsize(localPath):
            file = open(localPath, 'rb')
            self.ftp.storbinary('STOR '+remoteFile, file)
            file.close()
        return True
    def upload(self,localPath,remoteDir):
        if not self.exists(remoteDir):
            print remoteDir
            return False
        else:
            remoteDir = self.canonical(remoteDir)
        print remoteDir
            
        localPath = os.path.abspath(localPath)
        try:
            if os.path.isfile(localPath):
                self.uploadFile(localPath,remoteDir,check=False)
            elif os.path.isdir(localPath):
                dirName = localPath.rsplit('\\')[-1]
                if not self.mkdir(dirName):
                    return False
                for filename in os.listdir(localPath):
                    subLocal = localPath+'\\'+filename
                    subRemote = self.canonical(remoteDir+'/'+dirName)
                    self.upload(subLocal,subRemote)
            else:
                return False
            return True
        except:
            sys.excepthook(*sys.exc_info())
            return False
    def downloadFile(self,remotePath,localDir,localName='',check=True):
        print remotePath
        if check and not self.type(remotePath)=='-':
            print 'not file'
            return False
        elif not localName:
            localName = remotePath.rsplit('/',1)[-1]
        
        if check and not os.path.exists(localDir):
            print 'no local directory'
            return False
        else:
            localFile = localDir+'\\'+localName
        
        if localName not in os.listdir(localDir) or self.ftp.size(remotePath) != os.path.getsize(localFile):
            bufsize = 1024
            file = open(localFile, 'wb')
            self.ftp.retrbinary('RETR '+remotePath, file.write, bufsize)
            file.close()
        return True
    def download(self, remotePath, localDir, type=None):
        if not os.path.exists(localDir):
            return False
        else:
            localDir = os.path.abspath(localDir)
        print localDir
        
        remotePath = self.canonical(remotePath)
        try:
            if not type:
                type = self.type(remotePath)
            if type=='-':
                self.downloadFile(remotePath,localDir,check=False)
            elif type=='d':
                remoteName = remotePath.rsplit('/',1)[-1] if remotePath!='/' else 'root'
                subLocal = localDir+'\\'+remoteName
                subRemote = self.ls(remotePath)
                if not os.path.exists(subLocal):
                    os.mkdir(subLocal)
                if not os.path.isdir(subLocal):
                    return False
                for file in subRemote['-']:
                    self.downloadFile(remotePath+'/'+file,subLocal,check=False)
                for dir in subRemote.get('d',set()):
                    self.download(remotePath+'/'+dir,subLocal,'d')
            else:
                return False
            return True
        except:
            sys.excepthook(*sys.exc_info())
            return False
    def close(self):
        self.ftp.set_debuglevel(0) #關閉除錯模式
        self.ftp.close() #退出ftp
    #做刪掉檔案的動作(遞迴)
    # def delete_check_retain(self,a,path):
        # path = a
        # self.cd(a)
        # tmp = self.ls("dir")
        # print "/"*105
        # print tmp
        # print "-"*105
        # for p in tmp:
            # if tmp.get(p) == "file":
                    # try:
                        # self.delete(p)
                    # except:
                        # print "delete fail!!!"
            # else:
                # self.delete_check_retain(p,path)
            # self.cd("..")
            # self.rmd(path)
    # def delete_file(self,a,path):
        # if a.find('.')!= -1:
            # try:
                # self.delete(a)
            # except:
                # print "delete fail!!!"
        # else:
            # tmp = self.ls("dir")
            # print tmp
            # print "a"*105
            # print tmp.get(a)
            # if tmp.get(a) == "dir":
                # print "/"*105
                # path = path.replace(a+"/","")
                # self.delete_check_retain(a,path)
        
def test():
    ftp = main()
    ftp.login(
        "dmftp.insynerger.com",
        2100,
        "insynerger",
        "vu84y9352883637",
    )
    
if __name__ == '__main__':
    test()

'''
import h_ftp
ftp = h_ftp.main()
ftp.login(
    "dmftp.insynerger.com",
    2100,
    "insynerger",
    "vu84y9352883637",
)
ftp.cd('igw')
ftp.download('_common',r'C:\Users\user\Desktop\ftp test')
'''