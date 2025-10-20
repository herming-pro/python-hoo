import os
import sys
from copy import deepcopy

class OpenError_Wrong_FORMAT(Exception): pass

class data(dict):
    """
    a
    b
    c
    data = {default:['a','b','c']}
    
    a=1
    a=2
    a=3
    data = {a:['1','2','3']}
    
    a=1
    b=2
    c=3
    data = {a:['1'],b:['2'],c:['3']}
    """
    def add(self,data):
        if "=" in data:
            key,value = data.split("=",1)
        else:
            key,value = None, data

        if key in self:
            self[key].append(value)
        else:
            self.update({key:[value]})
    def get(self,key = None, default = []):
        return dict.get(self,key,default)
class main():
    def __init__(self,dir=None,extension='.her'):
        self.__dir = os.path.abspath(dir)
        self.extension = extension
        self.__fileData = {}
        self.__comment = ["#"]
        self.prevPath = ""
    def set_extension(extension): self.extension = extension
    def set_dir(self,dir): self.__dir = os.path.abspath(dir)
    def read(self,fileName):
        absPath = self.__absPath(fileName)
        if not os.path.exists(absPath):
            return False
        elif absPath in self.__fileData:
            restore = self.__fileData[absPath]
        else:
            restore = None
            
        self.__fileData[absPath] = {}
        try:
            file = open(absPath)
            tmpfileData = data()
            self.__fileData[absPath][''] = tmpfileData
            for line in file.readlines():
                line = line.rstrip()
                if line and not (line[0] in self.__comment):
                    if  line[0] == "[":
                        tag = line.split("[",1)[1].split("]",1)[0] 
                        tmpfileData = data()
                        self.__fileData[absPath][tag] = tmpfileData
                    else:
                        tmpfileData.add(line)
            file.close()
        except Exception:
            if restore==None:
                self.__fileData.pop(absPath)
            else:
                self.__fileData[absPath] = restore
            sys.excepthook(*sys.exc_info())
            return False
            
        self.prevPath = absPath
        return True
    def get(self,fileName = "",tag=None,reload=False):
        absPath = self.__absPath(fileName)
        if absPath not in self.__fileData:
            return None
        if reload==True:
            self.read(absPath)
        if tag==None:
            return deepcopy(self.__fileData.get(absPath,{}))
        else:
            return deepcopy(self.__fileData.get(absPath,{}).get(tag,False))
    def get_filename(self,):
        return {path:path.rsplit('\\',1)[-1][:-len(self.extension)] for path in self.__fileData}
    def save(self,data,fileName='',tag=None):
        absPath = self.__absPath(fileName)
        if absPath not in self.__fileData and (not os.path.isdir(os.path.dirname(absPath)) or tag):
            return False
        if tag == None:
            self.__fileData[absPath] = deepcopy(data)
            return True
        elif tag in self.__fileData[absPath]:
            self.__fileData[absPath][tag] = deepcopy(data)
            return True
        else:
            return False
    def write(self,fileName='',*tags):
        def write_tag(tag,filedata,save):
            single = []
            multi = []
            if 'default' in filedata[tag]:
                if len(filedata[tag]['default'])>1:
                    tmp = multi
                    tmp.append('\n')
                else:
                    tmp = single
                for value in sorted(filedata[tag]['default']):
                    tmp.append(value+'\n')
                filedata[tag].pop('default')
            for key in sorted(filedata[tag]):
                if len(filedata[tag][key])>1:
                    tmp = multi
                    tmp.append('\n')
                else:
                    tmp = single
                for value in sorted(filedata[tag][key]):
                    tmp.append('%s=%s\n'%(key,value))
            if single:
                save += '\n'
            save += single
            save += multi
        
        absPath = self.__absPath(fileName)
        if absPath not in self.__fileData:
            return None
        tags = self.__tags(absPath,*tags)
        
        filedata = self.__fileData[absPath]
        save = []
        if os.path.exists(absPath):
            try:
                newline = False
                reserve = False
                file = open(absPath)
                for line in file.readlines():
                    if not reserve and not line:
                        continue
                    
                    if line[0] in self.__comment:
                        reserve = False
                        # 與上一個tag間格一行
                        if newline:
                            save.append('\n')
                            newline = False
                        save.append(line)
                        
                    elif line[0]=='[':
                        tag = line.split('[',1)[1].split(']',1)[0]
                        save.append(line)
                        if tag in tags:
                            reserve = False
                            newline = True
                            if tag in filedata:
                                write_tag(tag,filedata,save)
                        else:
                            # 如果tag不在更新的tags裡 則保留原本的設定
                            reserve = True

                    elif reserve:
                        # 寫入原本設定
                        save.append(line)
                file.close()
            except Exception:
                self.read(absPath)
                sys.excepthook(*sys.exc_info())
                return False
        else:
            for tag in filedata:
                if tag in tags:
                    write_tag(tag,filedata,save)
        
        file = open(absPath,mode='w')
        for line in save:
            file.write(line)
        file.close()
        
        self.read(absPath)
        return True
    def clear(self,*fileNames):
        if not fileNames:
            self.__fileData.clear()
        for fileName in fileNames:
            absPath = self.__absPath(fileName)
            self.__fileData.get(absPath,{}).clear()
    def printer(self,fileName='',*tags):
        absPath = self.__absPath(fileName)
        if absPath not in self.__fileData:
            return
        tags = self.__tags(absPath,*tags)
        
        print '<%s>'%absPath
        filedata = self.__fileData[absPath]
        for tag in sorted(filedata):
            print '[%s]'%tag
            for key in sorted(filedata[tag]):
                for value in filedata[tag][key]:
                    print key+'='+value
    def __absPath(self,fileName):
        absPath = fileName.replace('/','\\')
        if absPath == '':
            return self.prevPath
        if not os.path.isabs(absPath):
            absPath = self.__dir + '\\' + absPath
        absPath = os.path.abspath(absPath)
        if not absPath.endswith(self.extension):
            absPath += self.extension
        # print 'origin: %s, abs: %s'%(fileName,absPath)
        return absPath if os.path.exists(absPath) else ''
    def __tags(self,relPath,*tags):
        if not tags:
            return set(self.__fileData[relPath].keys())
        tags = set(tags)
        for tag in list(tags):
            if tag not in self.__fileData[relPath]:
                tags.remove(tag)
                print 'tag [%s] not in file <%s>'%(tag,relPath)
        return tags
        
if __name__ == '__main__':
    h_open = main()
    h_open.set_dir("")
    h_open.read("config")
    data = h_open.fileData
    # for filename in data:
        # for tag in data[filename]:
            # for key in data[filename][tag]:
                # for value in data[filename][tag][key]:
                    # data[filename][tag].add(value)
    h_open.write("config")
    
