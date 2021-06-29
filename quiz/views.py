from django.shortcuts import render
from .models import Quiz,Question,Result,Answer
from django.template import RequestContext
from django.views import generic, View

from .models import Quiz
from django.views.generic import ListView
from django.http import JsonResponse
from syllabus.models import Lecture
from django.urls import reverse_lazy
import re
#

def Assessmentview(request):
    # quiz = Quiz.objects.filter(lecture_na__id=fk)
    quiz = Quiz.objects.all()
    return render(request,'quiz/assessment_view.html',{'obj':quiz})

def quiz_view(request,pk):
    quiz = Quiz.objects.get(pk=pk)
    result=Result.objects.values_list('score', flat=True).filter(quiz__id=pk)
    last_result=0
    if len(result) > 0:
        last_result = result.reverse()[len(result) - 1]

    return render(request,'quiz/results_view.html',{'obj':quiz,'result':last_result})


def quiz_data_view(request,pk):
    quiz = Quiz.objects.get(pk=pk)
    print(quiz.get_questions())

    questions=[]
    for q in quiz.get_questions():
        answers =[]
        for a in q.get_answers():
            answers.append(a.text)
        questions.append({str(q):answers})
    return JsonResponse({
        'data':questions,
        'time':quiz.time,
    })

def save_quiz_view(request,pk):
    if request.is_ajax():
        questions =[]
        data = request.POST
        data_ = dict(data.lists())
        data_.pop('csrfmiddlewaretoken')
        for k in data_.keys():
            question = Question.objects.get(text=k)
            questions.append(question)
        user = request.user
        quiz = Quiz.objects.get(pk=pk)
        score =0
        multiplier= 100 /quiz.number_of_questions
        multiplier=round(multiplier, 2)

        results =[]
        correct_answer=None

        for q in questions:
            a_selected = request.POST.get(str(q.text))
            if a_selected !="":
                question_answers = Answer.objects.filter(question=q)
                for a in question_answers:
                    if a_selected == a.text:
                        if a.correct:
                            score+=1
                            correct_answer=a.text
                    else:
                        if a.correct:
                            correct_answer=a.text
                results.append({str(q):{'correct_answer':correct_answer,'answered':a_selected}})
            else:
                results.append({str(q):'not answered'})
        score_=score*multiplier

        Result.objects.create(quiz=quiz,user=user,score=score_)

        if score_ >= quiz.required_score_to_pass:
            return JsonResponse({'passed':True,'score':score_,'results':results})
        else:
            return JsonResponse({'passed': False,'score':score_,'results':results})







# # Create your views here.
# def Assessmentview(request):
#     questions = Quiz.objects.all()
#
#
#     if request.method == 'POST':
#         answers = []
#         data = request.POST
#         data_ = dict(data.lists())
#         data_.pop('csrfmiddlewaretoken')
#
#         n=0
#         for k,v in data_.items():
#             nn = re.sub("\D", "", v[n])
#             answers.append(nn)
#             n+1
#
#
#         strings = [str(integer) for integer in answers]
#
#
#         numbers_answered = []
#         counter_n=0
#         for num in range(0,len(strings)):
#             n= re.sub("\D", "", strings[num])
#             counter_n=counter_n+1
#             try:
#                 numbers_answered.append(int(n))
#             except:
#                 print("It is not number the last value line 42 in view .py quiz app")
#
#         question_answers = Assessment.objects.values('answer')
#         correct_a_list_values_from_model= []
#         correct_l = []
#
#         for v in question_answers:
#             question_answers_value = Assessment.objects.values(v.get('answer').lower())
#             print(question_answers_value)
#
#             l = [integer for integer in question_answers_value]
#             correct_a_list_values_from_model.append(l)
#
#
#         for v in correct_a_list_values_from_model[0]:
#             for key, value in v.items():
#                 if value.isnumeric():
#                     correct_l.append(int(value))
#
#         # compare answers with the correct answers list
#         score = 0
#         multiplier = 100 / 5
#
#         for a in numbers_answered:
#
#              if a in correct_l:
#                  score=score+1
#
#         final= score * multiplier
#
#         user = request.user
#         Results.objects.create(learner=user, mark=final)
#
#         assess_result=Results.objects.values_list('mark', flat=True).filter(learner__id=user.id)
#         last_results=assess_result.reverse()[len(assess_result)-1]
#
#         return render(request, 'quiz/results_view.html', {'results': last_results})
#     else:
#         return render(request, 'quiz/assessment_view.html', {'questions': questions})
#
