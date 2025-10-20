import os
import sys
class main():
    def __init__(self,Language_date):
        self.data_path=os.path.dirname(sys.argv[0])
        if self.data_path=="":
            self.data_path='.'
        self.Language={}
        self.restart(Language_date)
    def restart(self , Language_date):
        Language=open("%s/Language/%s"%(self.data_path,Language_date),"r").readlines()
        for i in Language:
            if ':' in i  and i[0] != "#":
                self.Language.update({i.split(':')[0]:i.split(':',1)[1].split("\n")[0]})
    def get(self,name):
        return self.Language.get(name,name).decode("utf-8")
    def keys(self,):
        return self.Language.keys()
    def re_get(self,_name_):
        for name, age in self.Language.items():
            if age.decode("utf-8")==_name_:
                return name