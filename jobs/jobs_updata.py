import os
from datetime import datetime
import time
import json
import h_webapi
import sys
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
    
'''
class main():
    def do(self):
        self.log(self.dataList)
        if(len(self.dataList) != 6):
            return 
        self.nb     = self.dataList[0]
        ip          = self.dataList[1]
        path        = self.dataList[2]
        username    = self.dataList[3]
        passwd      = self.dataList[4]
        report      = self.dataList[5]
        self.send("status" , {"nb" : self.nb , "info" : "進行中"})
        api = h_webapi.main()
        api.init()
        url = "http://%s"%ip
        #設定MQTT
        self.send("status" , {"nb" : self.nb , "info" : "設定MQTT"})
        self.log("[set_mqtt_broker_path]")
        parameter = {
            "path"      :   path,
            "username"  :   username,
            "password"  :   passwd
        }
        self.log(parameter)
        api_path = "/set_mqtt_broker_path"
        static , data = api.post_data( parameter = parameter ,url = url , path = api_path , headers = {"Content-Type": "application/json"} )
        
        
        self.log(static)
        if(not static):
            self.sendFail()
            return
        self.log("[set_mqtt_broker_path]")
        self.log(data)
        if(json.loads(data).get("result" , 999)):
            self.sendFail()
            return
        time.sleep(2)  
        #設定report
        self.send("status" , {"nb" : self.nb , "info" : "設定report"})
        self.log("[set_report_period]")
        parameter = {
            "period" : report
        }
        self.log(parameter)
        api_path = "/set_report_period"
        static , data = api.post_data( parameter = parameter ,url = url , path = api_path , headers = {"Content-Type": "application/json"} )
        self.log(static)
        if(not static):
            self.sendFail()
            return
        self.log(data)
        if(json.loads(data).get("result" , 999)):
            self.sendFail()
            return
        req = {}
        time.sleep(2) 
        try:
            #取得info
            self.send("status" , {"nb" : self.nb , "info" : "取得info"})
            api_path = "/info"
            static , data = api.get_data(url = url , path = api_path )
            if(not static):
                self.sendFail()
                return
            data = json.loads(data)
            self.log(data)
            req.update({"mac" : data["id"]})
            req.update({"ver" : data["ver"]})
            time.sleep(2)  
            #取得MQTT
            self.send("status" , {"nb" : self.nb , "info" : "取得MQTT"})
            api_path = "/get_mqtt_broker_path"
            static , data = api.get_data(url = url , path = api_path )
            if(not static):
                self.sendFail()
                return
            data = json.loads(data)
            self.log(data)
            if(data.get("result" , 999)):
                self.sendFail()
                return
            req.update({"path"      : data["msg"]["path"]})
            req.update({"username"  : data["msg"]["username"]})    
            req.update({"passwd"    : data["msg"]["password"]})    
            time.sleep(2)  
            
            #取得report
            self.send("status" , {"nb" : self.nb , "info" : "取得report"})
            api_path = "/get_report_period"
            static , data = api.get_data(url = url , path = api_path )
            if(not static):
                self.sendFail()
                return
            data = json.loads(data)
            self.log(data)
            if(data.get("result" , 999)):
                self.sendFail()
                return
            req.update({"report"      : data["msg"]["period"]})
        except :
            self.Send('main','debug',sys.exc_info())
            self.send("status" , {"nb" : self.nb , "info" : "API回傳有問題"})
            return
        self.send("info"   , {"nb" : self.nb , "info" : True  ,  "data" : req })
    def sendFail(self):
        self.send("status" , {"nb" : self.nb , "info" : "設定失敗"})
        self.send("info"   , {"nb" : self.nb , "info" : False  ,  "data" : {"None" : ""} })