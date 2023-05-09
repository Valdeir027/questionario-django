import datetime
from django.test import TestCase
from django.utils import timezone
from .models import Question, Choice


class QuestionModelsTests(TestCase):
     
     def test_was_published_recently_with_future_question(self):
          #é possivel criar uma publicação recente em um dia no futuro
          #preciso resolver isso.
          time  = timezone.now() + datetime.timedelta(days = 30)
          future_question  = Question(pub_date = time)
          self.assertIs(future_question.was_published_recently(), False)