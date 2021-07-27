from django.shortcuts import render
from .models import Quiz,Result
from django.template import RequestContext
from django.views import generic, View

from .models import Quiz
from django.views.generic import ListView
from django.http import JsonResponse
from syllabus.models import Lecture
from django.urls import reverse_lazy
from assess_questions.models import  Question,Answer

import re
def Assessmentview(request):
    # quiz = Quiz.objects.filter(lecture_na__id=fk)
    quiz = Quiz.objects.all()
    return render(request,'quiz/assessment_view.html',{'obj':quiz})

def available_quiz_view(request,pk):
    quiz = Quiz.objects.get(pk=pk)

    return render(request,'quiz/results_view.html',{'obj':quiz})


def quiz_detail_view(request,pk):
    quiz = Quiz.objects.get(pk=pk)
    all_questions=[]
    for question in quiz.get_questions():
        print(question)
        answers =[]
        for answer in question.get_answers():
            answers.append(answer.answer_title)
        all_questions.append({str(question):answers})
    return JsonResponse({
        'data':all_questions,
        'time':quiz.quiz_time,
    })

def submit_quiz(request,pk):
    if request.is_ajax():
        all_questions =[]
        all_data = request.POST
        all_data_dic = dict(all_data.lists())
        all_data_dic.pop('csrfmiddlewaretoken')

        for key in all_data_dic.keys():
            question = Question.objects.get(question_title=key)

            all_questions.append(question)

        user = request.user
        quiz = Quiz.objects.get(pk=pk)
        score =0
        multiplier= 100 /quiz.questions_number
        multiplier=round(multiplier, 2)

        results =[]
        correct_answer=None

        for question in all_questions:

            a_selected = request.POST.get(str(question.question_title))

            if a_selected !="":
                question_answers = Answer.objects.filter(quiz_question=question)

                for answer in question_answers:

                    if a_selected == answer.answer_title:
                        if answer.is_correct:
                            score+=1
                            correct_answer=answer.answer_title
                    else:
                        if answer.is_correct:
                            correct_answer=answer.answer_title
                results.append({str(question):{'correct_answer':correct_answer,'answered':a_selected}})
            else:
                results.append({str(question):'not answered'})

        final_result=score*multiplier

        Result.objects.create(quiz=quiz,user=user,score=final_result)

        if final_result >= quiz.pass_score:
            return JsonResponse({'success':True,'score':final_result,'results':results})
        else:
            return JsonResponse({'success': False,'score':final_result,'results':results})


