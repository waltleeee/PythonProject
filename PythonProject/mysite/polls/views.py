from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json


@csrf_exempt
def index(request):
    print("SHOW REQUEST")
    print(request)
    print(request.method)
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
