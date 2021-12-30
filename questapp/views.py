from django.http import HttpResponse
from django.shortcuts import render
from django.views import View


# Create your views here.
def index(request):
    return HttpResponse("You're at the questapp index.")


def detail(request, question_id):
    return HttpResponse(f"You're looking at the question {question_id}.")


def results(request, question_id):
    return HttpResponse(f"You're looking at the results of question {question_id}.")


def vote(request, question_id):
    return HttpResponse(f"You're voting on question {question_id}.")


