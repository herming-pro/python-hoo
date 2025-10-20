import h_open
class IOError_CanNotFind_CONFIG(Exception): pass
class IOError_Config_READ(Exception): pass
class IOError_Config_LEN(Exception): pass
class data():
    def __init__(self):
        self.IDLIST = {}
        self.TAGCONFIG = {}
class h_devset_open():
    def __init__(self,):
        self.data = data()
        
        self.__open = h_open.main()
        self.__open.set_path("config")
        if self.__open.open("InsDevSet_default"):
            self.__set_default_tag(self.__set_idlist())
            self.__set_setting_tag()
        else:
            raise IOError_CanNotFind_CONFIG
    def __set_setting_tag(self):     
        _FUNCTION   = 0
        _ADDR       = 1
        
        _REQ = 0
        _RES = 1
        customize_tmp =  self.__open_file("customize tag")
        set_tmp = self.__open_file("set tag")
        for i in self.data.TAGCONFIG.keys():
            _set_data = set_tmp.get(i, [":"])[0].split(":")
            
            if len(_set_data) == 2:
                if _set_data[_FUNCTION] == "":
                    _set_data[_FUNCTION] = "0x06"
                if _set_data[_ADDR] == "":
                    _set_data[_ADDR] = "0"
                self.data.TAGCONFIG[i].update({"set":{  "function"  : _set_data[_FUNCTION],
                                                        "addr"      : _set_data[_ADDR]}})
            else:
                print _set_data
                raise IOError_Config_LEN
            _customize_data = customize_tmp.get(i, [":"])[0].split(":")   
            if len(_set_data) == 2:
                if _customize_data[_REQ] == "":
                    continue
                if _customize_data[_RES] == "":
                    _customize_data[_RES] = _customize_data[_REQ]
                self.data.TAGCONFIG[i].update({"customize":{  "res"  : _customize_data[_RES],
                                                              "req"  : _customize_data[_REQ]}})    
            else:
                print _customize_data
                raise IOError_Config_LEN
    def __set_default_tag(self,tag_list):
        _SLAVE      = 0
        _FUNCTION   = 1
        _ADDR       = 2
        tmp = self.__open_file("default tag")
        for i in tag_list:
            _data = tmp.get(i, ["::"])[0].split(":")
            if len(_data) == 3:
                if _data[_SLAVE] == "":
                    _data[_SLAVE] = "1"
                if _data[_FUNCTION] == "":
                    _data[_FUNCTION] = "0x03"
                if _data[_ADDR] == "":
                    _data[_ADDR] = "0"
                self.data.TAGCONFIG.update({i:{}})
                self.data.TAGCONFIG[i].update({"default":{  "slave"     : _data[_SLAVE] ,
                                                            "function"  : _data[_FUNCTION],
                                                            "addr"      : _data[_ADDR]}})
            else:
                print _data
                raise IOError_Config_LEN
    def __set_idlist(self,):
        _NAME = 0
        _GROUP = 1
        _TAG =  2
        tag_list = []
        tmp = self.__open_file("id list")
        for i in tmp.get():
            ID = "%06d"%len(self.data.IDLIST.keys())
            _data = i.split(":")
            if len(_data) == 3:
                self.data.IDLIST.update({ID:{   "name" : _data[_NAME], 
                                                "group" : _data[_GROUP],
                                                "tag"  : _data[_TAG]
                                            }})
                if not(_data[_TAG] in tag_list ):
                    tag_list.append(_data[_TAG])
                    
            else:
                print _data
                raise IOError_Config_LEN
        return tag_list
    def __open_file(self,path):
        tmp = self.__open.get(path)
        if tmp:
            return tmp
        else:
            raise IOError_Config_READ
def test():
        
        
    s = h_devset_open()
    for i in s.data.IDLIST.keys():
        print '%s : %s'%(i, s.data.IDLIST[i])
    print "-----"
    for i in s.data.TAGCONFIG.keys():
        print '%s : %s'%(i, s.data.TAGCONFIG[i])
if __name__ == '__main__':
   test()