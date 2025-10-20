# coding=utf-8
import serial
import socket
import time
class modbus:
    def __defalue_data(self):
        # serial params
        self.PARITY_NONE    = "N"
        self.PARITY_EVEN    = "E"
        self.PARITY_ODD     = "O"
        self.SEVENBITS      = 7
        self.EIGHTBITS      = 8
        self.STOPBITS_ONE   = 1
        self.STOPBITS_TWO   = 2
        # function codes
        self.Read_Coils             = 0x01
        self.Read_Discrete_Inputs   = 0x02
        self.Read_Holding_Registers = 0x03
        self.Read_INPUTS_Registers  = 0x04
        self.Write_Single_Coils     = 0x05
        self.Write_Single_Register  = 0x06
        # others
        self.RTUMODE    = "RTU"
        self.TCPMODE    = "TCP"
        self.errorcode  = ""
        self.result     = {'slave' : 0 , 'func' : 0  , 'value' : [] }
        # error codes
        self.__errorcode = {  
            1   : "Illegal function"  ,
            2   : "Illegal data address"  ,
            3   : "Illegal data value"  ,
            4   : "Slave equipment failure"  ,
            5   : "confirm"  ,
            6   : "Slave device is busy"  ,
            7   : "Slave device is busy"  ,
            8   : "Storage parity error"  ,
            10  : "Unavailable gateway path"  ,
            11  : "Gateway target device failed to respond"
        }
    def __init__(self,):
        self.__defalue_data()
        self.__mode = self.RTUMODE
        self.__link_static = False
        self.__recode   = ""
        self.__config     = {
            self.RTUMODE : {
                "config_par" : ["console" ,"baudrate" ,"parity" ,"bits" ,"stopbits" ,"timeout"],
                "config" : {
                    "console"   : None              ,
                    "baudrate"  : 9600              , 
                    "parity"    : self.PARITY_NONE  , 
                    "bits"      : self.EIGHTBITS    , 
                    "stopbits"  : self.STOPBITS_ONE , 
                    "timeout"   : 0.8               , 
                },
                "read"  : lambda : "",
                "write" : lambda : "",
            } ,
            self.TCPMODE : {
                "config_par": [ "IP", "port", "timeout" ],
                "config" : {
                    "IP"        : "",
                    "port"      : 502,
                    "timeout"   : 10
                },
                "read"  : lambda : "",
                "write" : lambda : "",
            } ,
        }
        self.__RTU_config = {}
        self.__TCP_config = {}
    # set_mode : support "RTU" or "TCP"
    def set_mode(self, mode):
        if mode in [ self.RTUMODE , self.TCPMODE]:
            self.__mode = mode
            return True
        return False
    # "RTU" : set_config(console, baudrate, parity, bits, stopbits, timeout)
    # "TCP" : set_config(IP, port, timeout)
    def set_config(self, *arg, **kw):
        if(len(arg) == 0 and kw == {}):
            return True
        tmp = self.__config[self.__mode]["config_par"]
        [self.__config[self.__mode]["config"].update({j: arg[i]}) for i , j in enumerate(tmp[:len(arg)]) ]
        [self.__config[self.__mode]["config"].update({j:  kw[j]}) for i , j in enumerate(tmp[len(arg):]) if kw.get(j , False)]
        print(self.__config[self.__mode]["config"])
        return True
    def link(self, *arg, **kw):
        self.set_config(*arg,**kw)
        try:
            config = self.__config[self.__mode]["config"]
            if self.__mode == self.RTUMODE:
                self._ser_=serial.Serial(
                        port        = config["console" ],
                        baudrate    = config["baudrate"],
                        parity      = config["parity"  ],
                        bytesize    = config["bits"    ],
                        stopbits    = config["stopbits"],
                        timeout     = config["timeout" ],
                    )
                self.__config[self.__mode]["read"]  = self._ser_.read
                self.__config[self.__mode]["write"] = self._ser_.write
            elif self.__mode == self.TCPMODE:
                self._ser_=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self._ser_.settimeout(config["timeout"])
                print(config["IP"])
                print(config["port"])
                self._ser_.connect((config["IP"] , config["port"]))
                self.__config[self.__mode]["read"]  = self._ser_.recv
                self.__config[self.__mode]["write"] = self._ser_.send
            else:
                return False
        except Exception as a:
            print(a.__class__, a)
            return False
        self.__link_static = True
        return True
    def close(self):
        self.__link_static = False
        try:
            self._ser_.close()
        except:
            pass
    # mbus_Send(slave, function, address, quantity)
    def mbus_Send(self, *arg, **kw):
        if self.__link_static:
            message, len = self.__combine(*arg, **kw)
            self.__mbus_send(message)
            return self.__mbus_read(len, message)
    def udf_Send(self, res, _len):
        if self.__link_static:
            self.__mbus_send(res + self.__crc(res))
            time.sleep(0.1)
            try:
                result = self._ser_.read(_len).encode('hex').upper()
                if not (result[-4:].upper() == self.__crc(result[:-4]).upper()):
                    self.errorcode = "CRC ERROR"
                    return False
                return result[:-4]
            except:
                return ""
    def __combine(self, slave, function, address, quantity = 1):
        if type(function) == str:
            function = int(function,16)
        if   function in [ self.Read_Coils , self.Read_Discrete_Inputs ]:
            nb = 1+1+1+int(quantity)/8+1
        elif function in [ self.Read_Holding_Registers , self.Read_INPUTS_Registers]:
            nb = 1+1+1+int(quantity)*2
        elif function in [ self.Write_Single_Register]:
            nb = 6
        elif function in [ self.Write_Single_Coils ]:
            quantity = quantity if int(quantity) == 0 else 0xFF00
            nb = 6
        else:
            message="function error"
            nb = -1
        if nb != -1 :
            message = '%02x%02x%04x%04x'%(slave , function , address , quantity)
        return message,nb + (2 if self.__mode == self.RTUMODE else 6)
    def __mbus_send(self, message):
        if self.__mode == self.RTUMODE:
            message += self.__crc(message)
        elif self.__mode == self.TCPMODE:
            message = '0001000000%02X%s'%(len(message)/2,message)
        self.__config[self.__mode]["write"](self.__decode_message(message))
        
    def __mbus_read(self, _len, message):
        self.errorcode = ""
        try:
            result = self.__config[self.__mode]["read"](_len).encode('hex').upper()
            
            # 檢查長度
            if self.__mode == self.RTUMODE:
                if not (len(result) == _len * 2 or len(result) == 5 * 2 ):
                    self.errorcode = "LEN ERROR"
                    return False , { 'value' : result }
                if not(result[-4:] == self.__crc(result[:-4])):
                    self.errorcode = "CRC ERROR"
                    return False , { 'value' : result }
                result = result[:-4]
            elif self.__mode == self.TCPMODE:
                if not (len(result) == _len * 2 or len(result) == 9 * 2 ):
                    self.errorcode = "LEN ERROR"
                    return False , { 'value' : result }
                result = result[6*2:]

            # 檢查站號
            tmp_res_slave = int(result[:2],16)
            tmp_mes_slave = int(message[:2],16)
            if not(tmp_res_slave == tmp_mes_slave):
                self.errorcode = "SLAVE ERROR"
                return False , { 'value' : result }
            # 檢查功能碼
            tmp_res_func = int(result[ 2:4],16)
            tmp_mes_func = int(message[2:4],16)
            if tmp_res_func - 0x80 == tmp_mes_func :
                tmp_r = int(result[4:6],16)
                self.errorcode = self.__errorcode.get(tmp_r,"function error")
                return False , result
            if not(tmp_res_func == tmp_mes_func ):
                self.errorcode = "FUNCTION ERROR"
                return False , { 'value' : result }
            self.result['slave']    = tmp_res_slave
            self.result['func']     = tmp_res_func
            self.result['value']    = []
            leng = int(result[4:6] , 16) if tmp_res_func != self.Write_Single_Register  else 0
            for i in xrange(leng):
                self.result['value'].append(result[6 + i * 2:8 + i * 2])
            return True , self.result
        except Exception as a:
            return False , { 'value' : "" }
    # CRC轉換
    def __crc(self, message):
        _crc_ = []
        for i in xrange(len(message) / 2):
            _crc_.append(int(message[0 + i * 2:2 + i * 2], 16))
        CRC_recode = bin(int("FFFF", 16))[2:].zfill(16)
        for i in _crc_:
            CRC_recode = bin(int(CRC_recode, 2) ^ i)[2:].zfill(16)
            for i in xrange(8):
                ans_me = CRC_recode[-1]
                CRC_recode = CRC_recode[:-1].zfill(16)
                if ans_me == "1":
                    CRC_recode = bin(int(CRC_recode, 2) ^ int("A001", 16))[2:].zfill(16)
        CRC_recode = CRC_recode[8:] + CRC_recode[:8]
        return hex(int(CRC_recode, 2))[2:].upper().zfill(4)
    # Hex(Base 16) decode
    def __decode_message(self, message):
        self.__recode = ""
        for i in xrange(len(message) / 2):
            self.__recode += chr(int(message[0 + i * 2:2 + i * 2], 16))
        return self.__recode

def test():
    t = modbus()
    t.set_mode(t.TCPMODE)
    t.set_config("192.168.10.43", port=502 , timeout=0.8)
    tmp = t.link()
    if tmp:
        static , data = t.mbus_Send(82, 03, 0x1000, 1)
        print(data , static)
    else:
        pass
    t.close()
    
if __name__ == '__main__':
    test()