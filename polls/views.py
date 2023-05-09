from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import Question, Choice
from django.template import loader
from django.http import Http404
from django.urls import reverse

def index(request):
    latest_question_list =  Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('polls/index.html')
    context= {
        'latest_question_list': latest_question_list,
    }
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
    try:
        question = Question.objects.get(pk = question_id)
    except Question.DoesNotExist:
        raise Http404("Questão não existe")
    
    return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return request(request,'polls/results.html', {'question': question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk= question_id)
    try:
        selected_chocie = question.choice_set.get(pk=request.POST['choice'])

    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html',{
            'question':question,
            'error_message': "Você não selecionou uma alternativa"
        })
    
    else:
        selected_chocie.votes +=1
        selected_chocie.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
