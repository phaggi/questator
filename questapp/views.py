from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import Question, Choice
from django.template import loader
from django.urls import reverse


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
    context = {'question': question}
    return render(request=request, template_name='questapp/detail.html', context=context)


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request=request, template_name='questapp/results.html', context=context)


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        context = {'question': question, 'error_message': "You didn't select a choice."}
        result = render(request=request, template_name='questapp/detail.html', context=context)
    else:
        selected_choice.votes += 1
        selected_choice.save()
        result = HttpResponseRedirect(reverse('questapp:results', args=(question_id,)))
    return result
