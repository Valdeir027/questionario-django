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


     def test_was_published_recently_old_question(self):
          #a função was_published_recently() retornna false se a data da publicação recente for de um dia atras

          time = timezone.now()- datetime.timedelta(days =1, seconds =1)
          old_question = Question(pub_date=time)
          self.assertIs(old_question.was_published_recently(), False)

     def test_was_published_recently_with_recent_question(self):
          # a função was_published_recently() retorna verdadeiro se a publição tiver a data de ate 23 horas atras
          time = timezone.now() - datetime.timedelta(hours=23,minutes=59,seconds=59)
          recent_Question = Question(pub_date = time)
          self.assertIs(recent_Question.was_published_recently(), True)