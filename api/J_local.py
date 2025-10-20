import os

class IOError(Exception): pass

class FileStructure():
    def __init__(self,):
        self.modules = {}
        self.packages = {}
        self.localPath = ''
    def __str__(self,):
        return self.printer()
    def printer(self,):
        TAB = ' '*4
        res = ''
        res += '<%s>'%self.localPath+'\n'
        modules = self.modules
        if 'common' in modules:
            res += '[common]\n'
            for item in modules['common'].items():
                res += TAB+' - '.join(item)+'\n'
        for platform in modules:
            if platform == 'common':
                continue
            res += '['+platform+']\n'
            if 'core' in modules[platform]:
                res += TAB+'core:\n'
                for item in modules[platform]['core'].items():
                    res += TAB*2+' - '.join(item)+'\n'
            if 'web' in modules[platform]:
                res += TAB+'web:\n'
                for item in modules[platform]['web'].items():
                    res += TAB*2+' - '.join(item)+'\n'
            res += TAB+'module:\n'
            for core in modules[platform]:
                if core in ['web','core']:
                    continue
                res += ' '.join([TAB*2,core])+'\n'
                for module in sorted(modules[platform][core]):
                    res += ' '.join([TAB*3,module,'-',modules[platform][core][module]])+'\n'
        return res
        
class main():
    def __init__(self,):
        self.files = FileStructure()
        self.localPath = './local'
        self.files.localPath = os.path.abspath(self.localPath)
        
        if os.path.exists(self.localPath):
            self.__scan_module()
            self.__scan_package()
        else:
            print '%s not exist'%self.localPath
            
        # print self.files
    def localPath(self,path):
        self.localPath = path
    def isdir(self,*paths):
        return os.path.isdir('/'.join(paths))
    def isfile(self,*paths):
        return os.path.isfile('/'.join(paths))
    def listdir(self,*paths):
        return os.listdir('/'.join(paths))
    def scan(self,mode):
        return {
            'modules':self.__scan_module,
        }.get(mode,lambda *args,**kw:False)()
    def __scan_module(self,):
        MODULEPATH = self.localPath+'/'+'module'
        COMMON = '_common'
        HEAD = 'igateway-v3-'
        END = '.tar.gz'
        
        if not os.path.exists(MODULEPATH):
            print 'File not exixt : '+'/'.join(MODULEPATH)
            return False
        
        self.files.modules.clear()
        modules = self.files.modules
            
        cores = self.listdir(MODULEPATH)
        modules['common'] = {}
        if COMMON in cores:
            cores.remove(COMMON)
            if self.isdir(MODULEPATH,COMMON):
                for filename in self.listdir(MODULEPATH,COMMON):
                    if filename=='install.sh' and self.isfile(MODULEPATH,COMMON,filename):
                        modules['common']['install.sh'] = ''
                    if not self.isfile(MODULEPATH,COMMON,filename) \
                    or not HEAD==filename[:len(HEAD)] \
                    or not filename.endswith(END):
                        continue
                    
                    splitname = filename[len(HEAD):-len(END)].split('-')
                    if len(splitname)!=4:
                        print 'Invaild name : %s'%filename
                        continue
                    type, name, c, r = splitname
                    moduleName = type+'-'+name
                    ver = c+'-'+r
                    if moduleName not in modules['common']:
                        modules['common'][moduleName] = ver
                    else:
                        modules['common'][moduleName] = max(modules['common'][moduleName],ver)
                
        for core in cores:
            if not self.isdir(MODULEPATH,core):
                continue
            for platform in self.listdir(MODULEPATH,core):
                if not self.isdir(MODULEPATH,core,platform):
                    continue
                if platform not in modules:
                    modules[platform] = {}
                modules[platform][core] = {}
                if 'core' not in modules[platform]:
                    modules[platform]['core'] = {}
                if 'web' not in modules[platform]:
                    modules[platform]['web'] = {}
                
                for filename in self.listdir(MODULEPATH,core,platform):
                    if not self.isfile(MODULEPATH,core,platform,filename)\
                    or not HEAD==filename[:len(HEAD)]\
                    or not filename.endswith(END):
                        continue
                        
                    splitname = filename[len(HEAD):-len(END)].split('-')
                    if len(splitname)!=4:
                        print 'Invaild name : %s'%filename
                        continue
                    type, name, c, r = splitname
                    if type=='core':
                        if c not in modules[platform]['core']:
                            modules[platform]['core'][c] = r
                        else:
                            modules[platform]['core'][c] = max(modules[platform]['core'][c],r)
                    elif type=='web':
                        moduleName = type+'-'+name
                        if moduleName not in modules[platform]['web']:
                            modules[platform]['web'][moduleName] = c+'-'+r
                        else:
                            modules[platform]['web'][moduleName] = max(modules[platform]['web'][moduleName],c+'-'+r)
                    elif c!=core:
                        print 'core version not match: %s %s'%(core,filename)
                        continue
                    else:
                        moduleName = type+'-'+name
                        if moduleName not in modules[platform][core]:
                            modules[platform][core][moduleName] = r
                        else:
                            modules[platform][core][moduleName] = max(modules[platform][core][moduleName],r)
                    
        return True
    def __scan_package(self,):
        pass
    def get(self,mode):
        return {
            'modules':self.files.modules,
            'packages':self.files.packages,
        }.get(mode,{})
    
def test():
    main().printer()
    
if __name__ == '__main__':
    test()
    
    
