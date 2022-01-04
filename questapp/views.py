from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from .models import Question, Choice
from django.urls import reverse
from django.views import generic


# Create your views here.
class IndexView(generic.ListView):
    template_name = 'questapp/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).exclude(choice=None).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'questapp/detail.html'

    def get_queryset(self):
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        )


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'questapp/results.html'


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
