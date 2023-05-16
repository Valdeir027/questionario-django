import datetime
from django.test import TestCase
from django.utils import timezone
from .models import Question, Choice
from django.urls import reverse


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


def create_question(question_text, days):
     #     Cria uma pergunta com o  'question_text'
     #      fornecido e publique o determidano número de dias compensando o até agora
     #     (negativo para questões publicadas até agora no passado, e positivo para questões que ainda não)
     time = timezone.now() + datetime.timedelta(days = days)
     return Question.objects.create(question_text = question_text, pub_date=time)


class QuestionIndexViewTests(TestCase):
     def test_no_questions(self):
          """
          If no questions exist, an appropriate message is displayed.
          """
          response = self.client.get(reverse('polls:index'))
          self.assertEqual(response.status_code, 200)
          self.assertContains(response, "No polls are available.")
          self.assertQuerysetEqual(response.context['latest_question_list'], [])

     def test_past_question(self):
          """
          Questions with a pub_date in the past are displayed on the
          index page.
          """
          question = create_question(question_text="Past question.", days=-30)
          response = self.client.get(reverse('polls:index'))
          self.assertQuerysetEqual(
               response.context['latest_question_list'],
               [question],
          )

     def test_future_question(self):
          """
          Questions with a pub_date in the future aren't displayed on
          the index page.
          """
          create_question(question_text="Future question.", days=30)
          response = self.client.get(reverse('polls:index'))
          self.assertContains(response, "No polls are available.")
          self.assertQuerysetEqual(response.context['latest_question_list'], [])

     def test_future_question_and_past_question(self):
          """
          Even if both past and future questions exist, only past questions
          are displayed.
          """
          question = create_question(question_text="Past question.", days=-30)
          create_question(question_text="Future question.", days=30)
          response = self.client.get(reverse('polls:index'))
          self.assertQuerysetEqual(
               response.context['latest_question_list'],
               [question],
          )

     def test_two_past_questions(self):
          """
          The questions index page may display multiple questions.
          """
          question1 = create_question(question_text="Past question 1.", days=-30)
          question2 = create_question(question_text="Past question 2.", days=-5)
          response = self.client.get(reverse('polls:index'))
          self.assertQuerysetEqual(
               response.context['latest_question_list'],
               [question2, question1],
          )


class QuestionDetailViesTests(TestCase):
     def test_future_question(self):
          #A exibição de detalhes de uma pergunta com um pub_date no futuro retorna um 404 not found.
          furute_question = create_question(question_text= 'questão no futuro', days=5)
          url = reverse('polls:detail', args = (furute_question.id,))
          response = self.client.get(url)
          self.assertEqual(response.status_code, 404)
     

     def test_past_question(self):
          past_question = create_question(question_text='Past question.', days=5)
          url =  reverse('polls:detail', args=(past_question.id,))
          response  = self.client.get(url)
          self.assertContains(response, past_question.question_text)

