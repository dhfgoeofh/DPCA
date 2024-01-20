import clr
import os
clr.AddReference("System")
clr.AddReference("System.Data")
from System.Data import Odbc
from System.Data import CommandType
from System.Data.Odbc import OdbcCommand, OdbcParameter
import System
from multipledispatch import dispatch
import time
from System.Collections.Generic import Dictionary
    

def write_PLC(address, value):
    path = os.getcwd()
    clr.AddReference(f'{path}\dll\PLC.dll')

    from PLC import PlcConnection
    instance = PlcConnection()
    connect = instance.openConnect("COM3", 9600, instance.getParity(), 8, instance.getStopBits())
    if connect:
        type1 = System.String
        type2 = System.Int32
        writeList = Dictionary[type1, type2]()
        writeList[address] = value
        writeResponse = instance.write(writeList)
        print(f"write is : {writeResponse}")

        instance.closeConnect() # 연결 끊기 
        return writeResponse # Bool?
    else:
        return connect

def read_PLC():
    path = os.getcwd()
    clr.AddReference(f'{path}\dll\PLC.dll')

    from PLC import PlcConnection
    instance = PlcConnection()
    ## CONNECT 
    connect = instance.openConnect("COM3", 9600, instance.getParity(), 8, instance.getStopBits())
    
    if connect:
        readList = ["%MW0", "%MW1", "%MW2"]
        readResponse = instance.read(readList)
        datas = dict()
        for item in readResponse:
            datas[item.Key] = item.Value
        print(datas)
        instance.closeConnect()
        return datas
    return connect



@dispatch(str)
def get_count(query):
    path = os.getcwd()
    clr.AddReference(f'{path}\dll\DPCA.dll')
    # from namespace이름 import class이름
    from DPCA import Class1
    # instacne 생성
    uid = "total"
    instance = Class1(uid)

    if instance.tryConnectDatabase(): # 접속 체크
        ## Query Execute 
        ds = instance.executeNonQuery(query)
        return ds 

@dispatch(str, dict)
def get_count(query, formData):
    path = os.getcwd()
    clr.AddReference(f'{path}\dll\DPCA.dll')
    # from namespace이름 import class이름
    from DPCA import Class1

    # instacne 생성
    uid = "total"
    instance = Class1(uid)

    if instance.tryConnectDatabase(): # 접속 체크
        ## Get Procedure
        procedureName = query ## Procedure Name, 'CALL 프로시저이름(파라미터);'

        param1 = Odbc.OdbcParameter("@p_PLC_ID", Odbc.OdbcType.VarChar) # 프로시저 선언 때 파라미터 이름, 해당 변수의 타입, 해당 변수의 사이즈
        param1.Value = list(formData.keys())[0] # 찾을 값

        param2 = Odbc.OdbcParameter("@p_DeviceAddress", Odbc.OdbcType.VarChar)
        param2.Value = formData[list(formData.keys())[0]]
        parameters = [param1,param2] # parameter ==> List 형식으로 (요구조건임)
        ds = instance.executeProcedure(procedureName, parameters) # 함수 실행
        ### 출력 양식 ### 
        rows = ds.Tables[0].Rows
        cols = ds.Tables[0].Columns
        ret = ""
        for row in range(len(rows)):
            for col in range(len(cols)):
                ret = ret + " " + str(rows[row][col])
            ret = ret + '\n'
        return ret #rows[몇번째 행][ds.Tables[0].Columns[몇번째 컬럼]] , @@@ds.Tables[0]은 고정@@@



@dispatch(str)
def queryFunc(query):
    path = os.getcwd()
    clr.AddReference(f'{path}\dll\DPCA.dll')
    # from namespace이름 import class이름
    from DPCA import Class1

    # instacne 생성
    uid = "total"
    instance = Class1(uid)

    if instance.tryConnectDatabase(): # 접속 체크
        ## Query Execute 
        ds = instance.executeQuery(query)
        ### 출력 양식 ### 
        rows = ds.Tables[0].Rows
        cols = ds.Tables[0].Columns
        ret = ""
        for row in range(len(rows)):
            for col in range(len(cols)):
                ret = ret + " " + str(rows[row][col])
            ret = ret + '\n'
        
        # ret = rows[0][ds.Tables[0].Columns[0]]
        return ret #rows[몇번째 행][ds.Tables[0].Columns[몇번째 컬럼]] , @@@ds.Tables[0]은 고정@@@

@dispatch(str, dict)
def queryFunc(query, formData):
    path = os.getcwd()
    clr.AddReference(f'{path}\dll\DPCA.dll')
    # clr.AddReference(r'C:/Users/DSL/Desktop/R&D/dll/DPCA.dll')
    # from namespace이름 import class이름
    from DPCA import Class1

    # instacne 생성
    uid = "total"
    instance = Class1(uid)
 
    if instance.tryConnectDatabase(): # 접속 체크
                                                               
        procedureName = query ## Procedure Name, 'CALL 프로시저이름(파라미터);'
   
        param1 = Odbc.OdbcParameter("@p_PLC_ID", Odbc.OdbcType.VarChar) # 프로시저 선언 때 파라미터 이름, 해당 변수의 타입, 해당 변수의 사이즈
        param1.Value = list(formData.keys())[0] # 찾을 값

        param2 = Odbc.OdbcParameter("@p_DeviceAddress", Odbc.OdbcType.VarChar)
        param2.Value = formData[list(formData.keys())[0]]
        parameters = [param1,param2] # parameter ==> List 형식으로 (요구조건임)
        ds = instance.executeProcedure(procedureName, parameters) # 함수 실행
        ### 출력 양식 ### 
        rows = ds.Tables[0].Rows
        cols = ds.Tables[0].Columns
        ret = ""
        for row in range(len(rows)):
            for col in range(len(cols)):
                ret = ret + " " + str(rows[row][col])
            ret = ret + '\n'
        return ret #rows[몇번째 행][ds.Tables[0].Columns[몇번째 컬럼]] , @@@ds.Tables[0]은 고정@@@

    

if __name__ == "__main__": 
    # print(get_count("SELECT * FROM DPCA"))
    # print(get_count("Call pr(?);", {'id' : 1}))
    print(get_count("CALL selectPLC(?, ?)", {"COM3" : "M1"}))
    # datas = read_PLC()
    # for data in list(datas.keys()):
    #     querys = f"INSERT INTO DPCA VALUES('COM3', '{data}', {datas[data]});"
    #     print(querys)
    #     inf = get_count(querys)
    #     print(inf)
    # write_PLC("M0", 0)