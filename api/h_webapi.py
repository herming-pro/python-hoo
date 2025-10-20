import time
import sys
import json
import requests
import os
import time
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()
class main():
    def init(self):
        self.__headers = {'Authorization': 'Basic YWRtaW46bm1paWk='}
        self.__url     = "https://192.168.10.26"
        self.__path    = "/api/config/test/get"
        self.__timeout = 10
    # kw 支援 : url , path , headers , timeout
    def changeInfo(self, **kw):
        self.__url , self.__path , self.__headers , self.__timeout = self.__get_info(kw)
    def get_data(self , parameter = {} , **kw):
        try:
            url , path , headers , timeout = self.__get_info(kw)
            return True, self.__get_req( requests.get( "%s%s%s"%(url, path, self.__changegetData(parameter)) , headers=headers , verify=False , timeout=timeout) )
        except Exception as a:
            return False , "%s%s"%(a.__class__, a)
    def post_data(self, parameter = {} , **kw):
        try:
            if isinstance(parameter, str):
                parameter = json.loads(parameter)
            url , path , headers , timeout = self.__get_info(kw)      
            return True, self.__get_req( requests.post( "%s%s"%(url, path) , headers=headers , verify=False , timeout=timeout , json=parameter) )
        except Exception as a:
            return False , "%s%s"%(a.__class__, a)
    def __changegetData(self, data):
        n = []
        for i in data.keys():
            n.append("%s=%s"%(i,data[i]))
        return "?%s"%"&".join(n) if len(n) else ""
    def __get_info(self , kw):
        self.__headers = kw.get("headers", self.__headers)
        return kw.get("url", self.__url) , kw.get("path", self.__path) , self.__headers , kw.get("timeout", self.__timeout)
    def __get_req(self , data):
        # print json.dumps(json.loads(data.text), indent=4, ensure_ascii=False, sort_keys=True)
        return json.dumps(json.loads(data.text), indent=4, ensure_ascii=False, sort_keys=True)
    
if __name__ == '__main__':
    test = main()
    test.init()
    url = "https://192.168.10.26"
    static , data = test.get_data(  url = url , path = "/api/config/test/get" )
    if(static):
        print(data)
    static , data = test.post_data( parameter = {"test" : "???"} ,url = url , path = "/api/config/test/set" , headers = {"Content-Type": "application/json"} )
    print(data)
        