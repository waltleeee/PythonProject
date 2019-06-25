from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import base64
import polls.serverCommand as serverCommand
from pymongo import MongoClient


class ServerData:
    Command = ""
    JsonData = ""


#REQUEST DATA
class RequestRegisterData:
    Account = ""
    Password = ""


class RequestLoginData:
    Account = ""
    Password = ""


class RequestLogoutData:
    UserID = ""


class RequestRecordData:
    CircultName = ""
    RequestCount = 0
    StartNumber = 0


class RequestUploadRecordData:
    CircultName = ""
    UserID = ""
    Time = ""


#RESPONSE DATA
class ResponseRegisterData:
    Status = 0


class ResponseLoginData:
    Status = 0
    UserID = ""


class ResponseLogoutData:
    Status = 0


class circultTimeData:
    Account = ""
    CircultName = ""
    Time = ""

    # def __jsonencode__(self):
    #     return {
    #         "Account": self.Account,
    #         "CircultName": self.CircultName,
    #         "Time": self.Time
    #     }

    def GetData(self):
        return {
            "Account": self.Account,
            "CircultName": self.CircultName,
            "Time": self.Time
        }


class ResponseRecordData:
    Status = 0
    RecordList = None


class ResponseUploadRecordData:
    Status = 0


# class AdvancedJSONEncoder(json.JSONEncoder):
#     def default(self, obj):
#         if hasattr(obj, '__jsonencode__'):
#             return obj.__jsonencode__()

#         if isinstance(obj, set):
#             return list(obj)

#         return json.JSONEncoder.default(self, obj)


def requestLoginWork(inJsonData):
    serverData = ServerData()
    serverData.Command = serverCommand.responseLogin

    loginData = RequestLoginData()
    loginDataString = json.loads(inJsonData)
    loginData.Account = loginDataString["Account"]
    loginData.Password = loginDataString["Password"]

    print("REQUEST LOGIN DATA:")
    print(loginData.Account)
    print(loginData.Password)

    #check can login or not

    #TEST
    responseLoginData = ResponseLoginData()
    responseLoginData.Status = 1
    responseLoginData.UserID = loginData.Account + "001"
    jsonData = json.dumps(vars(responseLoginData))

    serverData.JsonData = jsonData

    return serverData


def requestRegisterWork(inJsonData):
    serverData = ServerData()
    serverData.Command = serverCommand.responseRegister

    registerData = RequestRegisterData()
    registerDataString = json.loads(inJsonData)
    registerData.Account = registerDataString["Account"]
    registerData.Password = registerDataString["Password"]

    print("REQUEST REGISTER DATA:")
    print(registerData.Account)
    print(registerData.Password)

    #check can Register or not

    #TEST
    responseRegisterData = ResponseRegisterData()
    responseRegisterData.Status = 1
    responseRegisterData.UserID = registerData.Account + "001"
    jsonData = json.dumps(vars(responseRegisterData))

    serverData.JsonData = jsonData

    return serverData


def requestLogoutWork(inJsonData):
    serverData = ServerData()
    serverData.Command = serverCommand.responseLogout

    logoutData = RequestLogoutData()
    logoutDataString = json.loads(inJsonData)
    logoutData.UserID = logoutDataString["UserID"]

    print("REQUEST LOGOUT DATA:")
    print(logoutData.UserID)

    #check can logout or not

    #TEST
    responseLogoutData = ResponseLogoutData()
    responseLogoutData.Status = 1
    print(responseLogoutData)
    jsonData = json.dumps(vars(responseLogoutData))

    serverData.JsonData = jsonData

    return serverData


def requestRecordWork(inJsonData):
    serverData = ServerData()
    serverData.Command = serverCommand.responseRecord

    recordData = RequestRecordData()
    recordDataString = json.loads(inJsonData)
    recordData.CircultName = recordDataString["CircultName"]
    recordData.RequestCount = recordDataString["RequestCount"]
    recordData.StartNumber = recordDataString["StartNumber"]

    print("REQUEST RECORD DATA:")
    print(recordData.CircultName)
    print(recordData.RequestCount)
    print(recordData.StartNumber)

    #check can get record or not

    #TEST
    responseRecordData = ResponseRecordData()
    circultData0 = circultTimeData()
    circultData1 = circultTimeData()

    circultData0.Account = "WALT"
    circultData0.CircultName = "MuteCity"
    circultData0.Time = "1:14.133"
    circultData1.Account = "WALT2"
    circultData1.CircultName = "MuteCity"
    circultData1.Time = "1:15.256"

    data001 = circultData0.GetData()
    data002 = circultData1.GetData()

    responseRecordData.RecordList = []
    responseRecordData.RecordList.append(data001)
    responseRecordData.RecordList.append(data002)

    responseRecordData.Status = 1
    jsonData = json.dumps(vars(responseRecordData))
    serverData.JsonData = jsonData

    return serverData


def requestUploadRecordWork(inJsonData):
    serverData = ServerData()
    serverData.Command = serverCommand.responseUploadRecord

    recordData = RequestUploadRecordData()
    recordDataString = json.loads(inJsonData)
    recordData.CircultName = recordDataString["CircultName"]
    recordData.UserID = recordDataString["UserID"]
    recordData.StartNumber = recordDataString["StartNumber"]

    print("REQUEST RECORD DATA:")
    print(recordData.CircultName)
    print(recordData.UserID)
    print(recordData.StartNumber)

    #check can upload record or not

    #TEST
    responseUploadRecordData = ResponseUploadRecordData()

    responseUploadRecordData.Status = 1

    jsonData = json.dumps(vars(responseUploadRecordData))

    serverData.JsonData = jsonData

    return serverData


def requestErrorWork():
    return ""


commandFunctions = {
    serverCommand.requestLogin: requestLoginWork,
    serverCommand.requestLogout: requestLogoutWork,
    serverCommand.requestRegister: requestRegisterWork,
    serverCommand.requestRecord: requestRecordWork,
    serverCommand.requestUploadRecord: requestUploadRecordWork
}


@csrf_exempt
def index(request):
    print("SHOW REQUEST")
    baseString = str(request.body, encoding="utf-8")
    jsonString = base64.b64decode(baseString)

    serverData = ServerData()
    serverDataString = json.loads(jsonString)
    serverData.Command = serverDataString["Command"]
    serverData.JsonData = serverDataString["JsonData"]

    print(serverData)

    responseServerData = ServerData()
    if serverData.Command in commandFunctions.keys():
        responseServerData = commandFunctions[serverData.Command](
            serverData.JsonData)
    else:
        responseServerData.Command = serverCommand.requestError
        responseServerData.JsonData = requestErrorWork()

    responseJsonData = json.dumps(vars(responseServerData)).encode()
    responseBase64Data = base64.b64encode(responseJsonData)

    #TEST MONGO
    # client = MongoClient('mongodb://localhost:27017/')
    # db = client['test']
    # pythontestdb = db['pythontestdb']

    #TEST insert_one
    # insertData = {"Account": "walt", "Password": "1234", "UserID": ""}
    # postID = pythontestdb.insert_one(insertData)

    #TEST insert_many
    # insertDatas = [{
    #     "Account": "walt2",
    #     "Password": "1111",
    #     "UserID": ""
    # }, {
    #     "Account": "walt3",
    #     "Password": "2222",
    #     "UserID": ""
    # }]
    # result = pythontestdb.insert_many(insertDatas)
    # print(result.inserted_ids)

    #TEST find_one
    # testData = pythontestdb.find_one({"Account": "walt"})
    # print(users.find_one({"Account": "walt"}))
    # print(testData)
    # print(testData['Account'])
    # print(testData['Password'])
    # print(testData['UserID'])

    #TEST find
    # testDatas = pythontestdb.find({"Account": "walt"})
    # for data in testDatas:
    #     print(data)

    #TEST Counting
    # print(pythontestdb.count_documents({}))
    # print(pythontestdb.count_documents({"Account": "walt"}))

    #TEST update_one
    # needUpdateData = {"Account": "walt2"}
    # newData = {"$set": {"Password": "XXXX"}}
    # pythontestdb.update_one(needUpdateData, newData)

    #TEST update_many
    # needUpdateData2 = {"Account": "walt"}
    # newData2 = {"$set": {"Password": "ＷＷＷＷＷ"}}
    # pythontestdb.update_many(needUpdateData2, newData2)

    return HttpResponse(responseBase64Data)


def detail(request, question_id):
    return HttpResponse(
        "You're looking at question {id}.".format(id=question_id))


def results(request, question_id):
    return HttpResponse(
        "You're looking at the results of question {id}.".format(
            id=question_id))


def vote(request, question_id):
    return HttpResponse(
        "You're voting on question {id}.".format(id=question_id))
