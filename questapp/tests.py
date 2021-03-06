import datetime
from django.test import TestCase
from django.utils import timezone
from django.db import models
from django.urls import reverse

from .models import Question, Choice


# Create your tests here.
class QuestionModelTest(TestCase):
    def test_recently_published_with_future_question(self):
        future_time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=future_time)
        self.assertIs(future_question.recently_published(), False)

    def test_recently_published_with_old_question(self):
        previews_day_time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=previews_day_time)
        self.assertIs(old_question.recently_published(), False)

    def test_recently_published_with_recent_question(self):
        now_day_time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=now_day_time)
        self.assertIs(recent_question.recently_published(), True)

    def test_question_text_isinstance_str(self):
        question = Question()
        choice = Choice()
        self.assertIsInstance(question.question_text, (str,))
        self.assertIsInstance(choice.choice_text, (str,))

    def test_str_example_equal_question_text(self):
        question = Question()
        choice = Choice()
        self.assertEqual(str(question), question.question_text)
        self.assertEqual(str(choice), choice.choice_text)

    def test_votes_is_int(self):
        choice = Choice()
        self.assertIsInstance(choice.votes, int)


def create_question_wit_no_choices(question_text, days):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    question = Question.objects.create(question_text=question_text, pub_date=time)
    return question


def create_question(question_text, days):
    question = create_question_wit_no_choices(question_text, days)
    add_choices(question)
    return question


def add_choices(question: Question):
    question.choice_set.create(choice_text='test choice', votes=0)


class QuestionIndexViewTest(TestCase):
    def test_no_question(self):
        responce = self.client.get(reverse('questapp:index'))
        self.assertEqual(responce.status_code, 200)
        self.assertContains(responce, 'No polls are available')
        self.assertQuerysetEqual(responce.context['latest_question_list'], [])

    def test_past_question(self):
        create_question(question_text='Past question.', days=-30)
        responce = self.client.get(reverse('questapp:index'))
        self.assertQuerysetEqual(responce.context['latest_question_list'], ['<Question: Past question.>'])

    def test_future_question(self):
        create_question(question_text='Future question.', days=30)
        responce = self.client.get(reverse('questapp:index'))
        self.assertContains(responce, 'No polls are available.')
        self.assertQuerysetEqual(responce.context['latest_question_list'], [])

    def test_past_and_future_questions(self):
        create_question(question_text='Past question.', days=-30)
        create_question(question_text='Future question.', days=30)
        responce = self.client.get(reverse('questapp:index'))
        self.assertQuerysetEqual(responce.context['latest_question_list'], ['<Question: Past question.>'])

    def test_two_past_questions(self):
        create_question(question_text='Past question 1.', days=-30)
        create_question(question_text='Past question 2.', days=-5)
        responce = self.client.get(reverse('questapp:index'))
        self.assertQuerysetEqual(responce.context['latest_question_list'],
                                 ['<Question: Past question 2.>', '<Question: Past question 1.>'])

    def test_question_with_no_choises(self):
        question = create_question_wit_no_choices(question_text='Past question.', days=-30)
        print(f'choices:{question.choice_set.count()}')
        self.assertEqual(question.choice_set.count(), 0)

    def test_question_with_choice(self):
        question = create_question(question_text='Past question.', days=-30)
        print(f'choices:{question.choice_set.count()}')
        self.assertEqual(question.choice_set.count(), 1)


class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        future_question = create_question(question_text='Future question.', days=5)
        url = reverse(viewname='questapp:detail', args=(future_question.id,))
        responce = self.client.get(url)
        self.assertEqual(responce.status_code, 404)

    def test_past_question(self):
        past_question = create_question(question_text='Past question.', days=-5)
        url = reverse(viewname='questapp:detail', args=(past_question.id,))
        responce = self.client.get(url)
        self.assertContains(responce, past_question.question_text)
