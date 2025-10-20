import h_open
import sys
class FormatError(Exception):pass

class Config():
    def __init__(self):
        self.users = {}
        self.connections = {}
        self.FTPservers = {}
        
class main():
    def __init__(self,path="config"):
        self.config = Config()
        
        self.openfiles = h_open.main()
        self.openfiles.set_path(path)
        if self.openfiles.read("InstallTool_config"):
            self.__set_users()
            self.__set_connections()
            self.__set_FTPservers()
        
        # self.printer()
    def get_tag(self,tag):
        tmp = self.openfiles.get(tag)
        try:
            if tmp!=False:
                return tmp
            else:
                raise FormatError('Nonexist tag')
        except:
            sys.excepthook(*sys.exc_info())
            return False
    def set(self,tag):
        try:
            return {
                'users':self.__set_users,
                'connections':self.__set_connections,
                'FTPservers':self.__set_FTPservers,
            }.get(tag,lambda *args,**kw:False)()
        except:
            sys.excepthook(*sys.exc_info())
            return False
    def __set_users(self):
        self.config.users = {}
        tmpdata = self.get_tag('users')
        for name in tmpdata:
            if len(tmpdata[name])!=1:
                raise FormatError('Invalid data length',tmpdata[name])
            else:
                config = tmpdata[name][0].split(':')
                if len(config)!=3:
                    raise FormatError('Invalid data length',config)
                else:
                    supw,username,passwd = config
                    self.config.users[name] = {
                        'supw':supw,
                        'username':username,
                        'passwd':passwd,
                    }
        return True
    def __set_connections(self):
        self.config.connections = {}
        tmpdata = self.get_tag('connections')
        for platform in tmpdata:
            self.config.connections[platform] = {}
            for config in tmpdata[platform]:
                config = config.split(':')
                if len(config)!=3:
                    raise FormatError('Invalid data length',config)
                elif config[0] in self.config.connections[platform]:
                    raise FormatError("Repeated connection's name",config)
                else:
                    name,user_setting,port = config
                    if not (port.isdigit() and 0<=int(port)<=65535 and user_setting in self.config.users):
                        continue
                        
                    self.config.connections[platform][name] = {
                        'user_setting':user_setting,
                        'port':port,
                    }
        return True
    def __set_FTPservers(self):
        self.config.FTPservers = {}
        tmpdata = self.get_tag('FTPservers')
        for name in tmpdata:
            if len(tmpdata[name])!=1:
                raise FormatError('Invalid data length',tmpdata[name])
            else:
                config = tmpdata[name][0].split(':')
                if len(config)!=4:
                    raise FormatError('Invalid data length',config)
                else:
                    ip,port,user,passwd = config
                    if not port.isdigit() or not 0<=int(port)<=65535:
                        continue
                        
                    self.config.FTPservers[name] = {
                        'ip':ip,
                        'port':port,
                        'user':user,
                        'passwd':passwd,
                    }
        return True
    def save(self,tag,data):
        try:
            return {
                'users':self.__save_users,
                'connections':self.__save_connections,
                'FTPservers':self.__save_FTPservers,
            }.get(tag,lambda *args,**kw:False)(data)
        except:
            self.set(tag)
            sys.excepthook(*sys.exc_info())
            return False
    def __save_users(self,data):
        savedata = {}
        for name in data:
            savedata[name] = []
            user = data[name]
            keys = ['supw','username','passwd']
            savedata[name].append('%s:%s:%s'%tuple(user[key] for key in keys))
            
        self.openfiles.save(savedata,tag='users')
        return self.__write(tags='users')
    def __save_connections(self,data):
        savedata = {}
        for platform in data:
            savedata[platform] = []
            for name in data[platform]:
                connect = data[platform][name]
                keys = ['user_setting','port']
                savedata[platform].append(name+':%s:%s'%tuple((connect[key] for key in keys)))
        self.openfiles.save(savedata,tag='connections')
        return self.__write(tags='connections')
    def __save_FTPservers(self,data):
        savedata = {}
        for name in data:
            savedata[name] = []
            FTPserver = data[name]
            keys = ['ip','port','user','passwd']
            savedata[name].append('%s:%s:%s:%s'%tuple((FTPserver[key] for key in keys)))
        self.openfiles.save(savedata,tag='FTPservers')
        return self.__write(tags='FTPservers')
    def get(self,tag):
        return {
            'users':self.config.users,
            'connections':self.config.connections,
            'FTPservers':self.config.FTPservers,
        }.get(tag,None)
    def __write(self,fileName='',tags='all'):
        return self.openfiles.write(fileName=fileName,tags=tags)
    def printer(self,):
        print '[users]'
        users = self.config.users
        for name in users:
            print name,users[name]
        print '[connections]'
        connections = self.config.connections
        for platform in connections:
            print platform
            for name in connections[platform]:
                print '    ',name,connections[platform][name]
        print '[FTPservers]'
        FTPservers = self.config.FTPservers
        for name in FTPservers:
            print name,FTPservers[name]

def test():
    format = main('')
    
    for i,name in enumerate(format.config.users):
        format.config.users[name]['user'] = str(i)
    for platform in format.config.connections:
        for i,name in enumerate(format.config.connections[platform]):
            connect = format.config.connections[platform][name]
            connect['port'] = str(i*1000)
    for i,name in enumerate(format.config.FTPservers):
        format.config.FTPservers[name]['user'] = str(i)
    
    format.__save_users()
    format.__save_connections()
    format.__save_FTPservers()
    
    format.printer()
    
    format.write()
if __name__ == '__main__':
    test()
