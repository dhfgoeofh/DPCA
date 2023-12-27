import clr # pip install pythonnet
clr.AddReference("System.Data")
from System.Data import Odbc
from System.Data import CommandType
from System.Data.Odbc import OdbcCommand, OdbcParameter
clr.AddReference("System")
import System
from urllib import parse
from System.Collections.Generic import Dictionary
import os
import time

def get_PLC(): # PLC Total Test
    path = os.getcwd()
    clr.AddReference(f'{path}\dll\PLC.dll')

    from PLC import PlcConnection
    instance = PlcConnection()
    connect = instance.openConnect("COM3", 9600, instance.getParity(), 8, instance.getStopBits())
    print(f"connect : {connect}")
    
    ## 개별 읽기 예시
    readList = ["%MW0", "%MW1", "%MW2"]

    ## 연속 읽기 예시
    addressRead = "%MW001" # 읽기 시작할 데이터 주소
    lengthRead = 8 # 데이터 주소부터 읽을 데이터 수 

    ## 개별 쓰기 예시 
    type1 = System.String
    type2 = System.Int32
    writeList = Dictionary[type1, type2]()
    writeList['%MW004'] = 43507
    writeList['%MW001'] = 43507

    # 연속 쓰기 예시 
    addressWrite = "%MW0"
    dataList = [9735, 57153, 27816]

    #개별 읽기 실행, Dict<String, Int>
    readResponse = instance.read(readList)
    print("readResponse")
    for item in readResponse:
        print(item.Key, item.Value)
    time.sleep(1)

    # 연속 읽기 실행, String, Int
    readSequentialResponse = instance.readSequential(addressRead, lengthRead)
    print("readSequentialResponse")
    for item in readSequentialResponse:
        print(item.Key, item.Value)
    time.sleep(1)

    # 개별 쓰기 : String[]
    writeResponse = instance.write(writeList)
    print(f"write is : {writeResponse}")

    ## 연속 쓰기 실행 String, Int[]
    writeSequentialResponse= instance.writeSequential(addressWrite, dataList)
    print(f"writeSequential is : {writeSequentialResponse}")

    instance.closeConnect()

def test(): # Database Test 
    # Add a reference to your DLL
    path = os.getcwd()
    clr.AddReference(f'{path}\dll\DPCA.dll')
    # from NAMESPACE import CLASS
    from DPCA import Class1
    uid = "total"
    query = "SELECT * FROM Member where name='zzzz!'"
    p = Class1(uid)
    result = p.executeNonQuery(query)
    print(result)

def test2(): # web API TEST 
    path = os.getcwd()
    clr.AddReference(f'{path}\dll\web.dll')
    # from NAMESPACE import CLASS
    from web import Program
    p = Program()
    result = p.get("http://127.0.0.1:5000/count/SELECT%20*%20FROM%20DPCA%3B/%20") # 
    print(result)

    ## PROCEDURE
    testDict = {"COM3" : "M1"}
    from System.Collections.Generic import Dictionary
    type1 = System.String
    type2 = System.String
    formData = Dictionary[type1, type2]()
    for item in list(testDict.keys()):
        formData[item] = testDict[item]
    result = p.delete(f"http://127.0.0.1:5000/api/{parse.quote('CALL selectPLC(?,?)')}", formData)
    print(result)

def total_test():
    # dll 연결
    path = os.getcwd()
    clr.AddReference(f'{path}\dll\DPCA.dll')
    # from namespace이름 import class이름
    from DPCA import Class1

    # instacne 생성
    uid = "total"
    instance = Class1(uid)

    if instance.tryConnectDatabase(): # 접속 체크

        ## TEST Query
        query = "SELECT * FROM Member"

        ## 몇 행 있는지 체크
        ds = instance.executeNonQuery(query) # 행 개수 체크하는 함수
        print(ds)
        ## Test SELECT / query 후 dataset 받아오기
        ds = instance.executeQuery(query)
        rows = ds.Tables[0].Rows # 출력 테스트 양식 
        print(rows[2][ds.Tables[0].Columns[0]]) #rows[몇번째 행][ds.Tables[0].Columns[몇번째 컬럼]] , @@@ds.Tables[0]은 고정@@@
       
        ## Test Procedure
        procedureName = "CALL TEST1(?);" ## Procedure Name, 'CALL 프로시저이름(파라미터);'
        param1 = Odbc.OdbcParameter("@input_id", Odbc.OdbcType.NVarChar, 10) # 프로시저 선언 때 파라미터 이름, 해당 변수의 타입, 해당 변수의 사이즈
        param1.Value = '1' # 찾을 값
        parameters = [param1] # parameter ==> List 형식으로 (요구조건임)
        ds = instance.executeProcedure(procedureName, parameters) # 함수 실행
        rows = ds.Tables[0].Rows
        print(rows[0][ds.Tables[0].Columns[0]])



if __name__ == "__main__":
    # result_dict = dotnet_query()
    # print(result_dict)
    test2()