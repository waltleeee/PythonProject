from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import base64
import polls.serverCommand as serverCommand
import datetime
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


class RequestRankData:
    CircultName = ""
    RequestCount = 0
    StartNumber = 0
    UserID = ""


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


class ResponseRankData:
    CircultName = ""
    Status = 0
    RankList = None


class ResponseUploadRecordData:
    Status = 0


# class AdvancedJSONEncoder(json.JSONEncoder):
#     def default(self, obj):
#         if hasattr(obj, '__jsonencode__'):
#             return obj.__jsonencode__()

#         if isinstance(obj, set):
#             return list(obj)

#         return json.JSONEncoder.default(self, obj)

client = MongoClient('mongodb://localhost:27017/')
checkLimit = 5
muteCityRankList = []
muteCityEXRankList = []


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

    responseLoginData = ResponseLoginData()

    #check can login or not
    db = client['test']
    users = db['users']

    if users.count_documents({"Account": loginData.Account}) != 0:
        user = users.find_one({"Account": loginData.Account})
        if user['Password'] != loginData.Password:
            responseLoginData.Status = 2
        else:
            responseLoginData.Status = 1
            responseLoginData.UserID = "&&%" + loginData.Account
            needUpdateData = {"Account": loginData.Account}
            newData = {
                "$set": {
                    "UserID": responseLoginData.UserID,
                    "LastActTime": datetime.datetime.now()
                }
            }
            users.update_one(needUpdateData, newData)
    else:
        responseLoginData.Status = 2

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

    responseRegisterData = ResponseRegisterData()

    #check can Register or not
    db = client['test']
    users = db['users']

    if users.count_documents({"Account": registerData.Account}) != 0:
        responseRegisterData.Status = 2
    elif users.count_documents({"Password": registerData.Password}) != 0:
        responseRegisterData.Status = 3
    else:
        newUserData = {
            "Account": registerData.Account,
            "Password": registerData.Password,
            "UserID": "-1",
            "LastActTime": datetime.datetime.now(),
            "RegisterTime": datetime.datetime.now()
        }
        oid = users.insert_one(newUserData)
        if oid != None:
            responseRegisterData.Status = 1
        else:
            responseRegisterData.Status = -1

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

    responseLogoutData = ResponseLogoutData()

    responseLogoutData = ResponseLogoutData()

    #check can logout or not
    db = client['test']
    users = db['users']

    if users.count_documents({"UserID": logoutData.UserID}) != 0:
        responseLogoutData.Status = 1
        needUpdateData = {"UserID": logoutData.UserID}
        newData = {
            "$set": {
                "UserID": "-1",
                "LastActTime": datetime.datetime.now()
            }
        }
        users.update_one(needUpdateData, newData)
    else:
        responseLogoutData.Status = -3

    jsonData = json.dumps(vars(responseLogoutData))

    serverData.JsonData = jsonData

    return serverData


def CheckIsCircultNameExist(inCircultName):
    if inCircultName == "muteCity":
        return True
    elif inCircultName == "muteCityEX":
        return True
    else:
        return False


def checkOverTime(inCheckTime):

    print("CHECK OVER TIME")
    print(checkLimit)
    nowTime = datetime.datetime.now()
    if nowTime - inCheckTime > datetime.timedelta(seconds=checkLimit):
        return True
    else:
        return False


def makeTimePoint(inMinute, inSecond, inMS):
    try:
        minute = int(inMinute)
        second = int(inSecond)
        ms = int(inMS)
        return (minute * 100000) + (second * 1000) + (ms)
    except ValueError:
        return 9999999


def sortRecord(inRecords):

    if len(inRecords) == 0:
        return inRecords

    smallIndex = 0
    checkIndex = 0
    tempRecord = None

    #find most fast timePoint
    for i in range(len(inRecords)):
        smallIndex = i
        checkIndex = smallIndex + 1
        while checkIndex <= (len(inRecords) - 1):
            if inRecords[checkIndex]["TimePoint"] < inRecords[smallIndex][
                    "TimePoint"]:
                smallIndex = checkIndex
            checkIndex += 1

        if smallIndex != i:
            tempRecord = inRecords[smallIndex]
            inRecords[smallIndex] = inRecords[i]
            inRecords[i] = tempRecord

    return inRecords


def getCircultID(inCircultName):
    if inCircultName == "muteCity":
        return "1000"
    elif inCircultName == "muteCityEX":
        return "1001"
    else:
        return ""


def getRankList(inCircultName, inStartIndex, inNeedCount):
    origionRankList = []
    if inCircultName == "muteCity":
        origionRankList = muteCityRankList
    elif inCircultName == "muteCityEX":
        origionRankList = muteCityEXRankList

    if len(origionRankList) > 0 and len(origionRankList) > inStartIndex:
        size = 0
        if len(origionRankList) >= (inStartIndex + inNeedCount):
            size = inNeedCount
        else:
            size = (len(origionRankList) - inStartIndex)

        rankList = []
        index = inStartIndex

        while len(rankList) < size:
            rankList.insert(len(rankList), origionRankList[index])
            index += 1

        # for i:=inStartIndex;i<len(origionRankList);i++{
        # 	rankList[index]=origionRankList[i]
        # 	index++

        # 	if index>=size{
        # 		break
        # 	}
        # }

        print("SIZE")
        print(size)
        print("RANKLIST")
        print(rankList)

        return rankList
    else:
        return origionRankList


def updateLocalRankList(inCircultName, inRankList):
    if inCircultName == "muteCity":
        global muteCityRankList
        muteCityRankList = inRankList
    elif inCircultName == "muteCityEX":
        global muteCityEXRankList
        muteCityEXRankList = inRankList


def InitialRankList():
    db = client['test']
    rankCollection = db['muteCityRank']
    circultID = getCircultID("muteCity")
    rankResult = rankCollection.find_one({"ID": circultID})


def requestRankWork(inJsonData):
    serverData = ServerData()
    serverData.Command = serverCommand.responseRank

    rankData = RequestRankData()
    rankDataString = json.loads(inJsonData)
    rankData.CircultName = rankDataString["CircultName"]
    rankData.RequestCount = rankDataString["RequestCount"]
    rankData.StartNumber = rankDataString["StartNumber"]
    rankData.UserID = rankDataString["UserID"]

    print("REQUEST RECORD DATA:")
    print(rankData.CircultName)
    print(rankData.RequestCount)
    print(rankData.StartNumber)
    print(rankData.UserID)

    responseRankData = ResponseRankData()
    responseRankData.RankList = []
    #check can get record or not

    db = client['test']
    users = db['users']

    if users.count_documents({"UserID": rankData.UserID}) != 0:
        if CheckIsCircultNameExist(rankData.CircultName) == False:
            print("REQUEST RANK CIRCULT NAME ERROR")
            responseRankData.Status = -2
        else:
            print("REQUEST RANK CIRCULT NAME OK")

            rankUpdateTime = db['circultUpdateTime']
            responseRankData.CircultName = rankData.CircultName
            updateTimeResult = rankUpdateTime.find_one(
                {"circultName": rankData.CircultName})

            if updateTimeResult != None:

                print("UPDATE TIME RESULT")
                print(updateTimeResult['circultName'])
                print(updateTimeResult['LastUpdateTime'])
                print(type(updateTimeResult['LastUpdateTime']))
                print(checkOverTime(updateTimeResult['LastUpdateTime']))

                if checkOverTime(updateTimeResult['LastUpdateTime']):
                    print("NEED UPDATE LAST UPDATE TIME")
                    needUpdateData = {"circultName": rankData.CircultName}
                    newData = {
                        "$set": {
                            "LastUpdateTime": datetime.datetime.now()
                        }
                    }
                    rankUpdateTime.update_one(needUpdateData, newData)

                    circultRecord = db[rankData.CircultName]
                    allRecord = circultRecord.find({})
                    records = []
                    for data in allRecord:
                        print(data)
                        time = data['Time'].split(':')
                        record = {
                            "Account": data['Account'],
                            "Time": data['Time'],
                            "TimePoint": makeTimePoint(time[0], time[1],
                                                       time[2])
                        }
                        records.insert(0, record)

                    #print(records)

                    records = sortRecord(records)

                    #print(records)

                    rankDataList = []

                    for i in range(len(records)):
                        data = {
                            "Account": records[i]['Account'],
                            "Time": records[i]['Time'],
                            "Rank": i + 1
                        }
                        rankDataList.insert(len(rankDataList), data)

                    print("RANK DATA LIST")
                    print(rankDataList)

                    circultID = getCircultID(rankData.CircultName)
                    rankCollection = db[rankData.CircultName + 'Rank']
                    updateCondition = {"ID": circultID}
                    newRankList = {"$set": {"RankList": rankDataList}}
                    rankCollection.update_one(updateCondition, newRankList)

                    updateLocalRankList(rankData.CircultName, rankDataList)
                    # print("SHOW LOCAL RANK LIST")
                    # print(muteCityRankList)
                    # print(muteCityEXRankList)
                else:
                    print("UPDATE RANK TIME LIMIT NOT REACH")

                responseRankData.RankList = getRankList(
                    rankData.CircultName, rankData.StartNumber,
                    rankData.RequestCount)
                responseRankData.Status = 1
            else:
                print("DB HAVE NO CIRCULT UPDATE TIME DATA")
                responseRankData.Status = -1
    else:
        print("NO USER, NO REQUEST RECORD")
        responseRankData.Status = -3

    jsonData = json.dumps(vars(responseRankData))
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
    serverCommand.requestRank: requestRankWork,
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
    #db = client['test']
    #pythontestdb = db['pythontestdb']

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
    #testDatas = pythontestdb.find({"Account": "walt"})
    #for data in testDatas:
    #    print(data)

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
