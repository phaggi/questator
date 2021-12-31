from django.http import Http404
from django.shortcuts import render
from django.views import View
from .models import Question
from django.template import loader


# Create your views here.
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('questapp/index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    return render(request, 'questapp/index.html', context)


def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoNotExist:
        raise Http404('Question does not exist')
    return render(request=request, template_name='questapp/detail.html', context={'question': question})


def results(request, question_id):
    return HttpResponse(f"You're looking at the results of question {question_id}.")


def vote(request, question_id):
    return HttpResponse(f"You're voting on question {question_id}.")


