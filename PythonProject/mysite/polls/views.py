from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import base64


@csrf_exempt
def index(request):
    print("SHOW REQUEST")
    baseString = bytes.decode(request.body)
    jsonString = base64.decodestring(baseString)
    print(baseString)
    print(jsonString)
    return HttpResponse("Hello, world. You're at the poll index.")


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
