from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import base64
import polls.serverCommand as serverCommand


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


class ResponseRecordData:
    Status = 0
    RecordList = []


class ResponseUploadRecordData:
    Status = 0


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

    #check can login or not

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

    #check can login or not

    #TEST
    responseLogoutData = ResponseLogoutData()
    responseLogoutData.Status = 1

    jsonData = json.dumps(vars(responseLogoutData))

    serverData.JsonData = jsonData

    return serverData


def requestRecordWork(inJsonData):
    responseRecordData = ResponseRecordData()
    return responseRecordData


def requestUploadRecordWork(inJsontData):
    responseUploadRecordData = ResponseUploadRecordData()
    return responseUploadRecordData


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
