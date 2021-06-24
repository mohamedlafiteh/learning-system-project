from django.shortcuts import render
from django.template import RequestContext
from django.views import generic, View

from .models import Quiz
from django.views.generic import ListView
from django.http import JsonResponse
from questions.models import  Question,Answer
from results.models import  Result
from django.urls import reverse_lazy


# class QuizListView(ListView):
#     model = Quiz
#     template_name = 'quizes/main.html'


def QuizListView(request,fk):
    quiz = Quiz.objects.get(lecture_na_id=fk)
    return render(request,'quizes/main.html',{'obj':quiz})
#
# class QuizListView (View):
#     response_template='quizes/main.html'
#     model = Quiz
#     quiz = Quiz.objects.get(lecture_na_id=8)
#
#     def get(self, request, *args, **kwargs):
#         context = locals()
#         context['quiz'] = self.quiz
#         return render(request,self.response_template, context)



# def select_quiz_view(request,fk):
#     quiz = Quiz.objects.get(lecture_na_id=fk)
#     return render(request,'quizes/v.html',{'obj':quiz})

def quiz_view(request,pk):

    quiz = Quiz.objects.get(pk=pk)
    return render(request,'quizes/quiz.html',{'obj':quiz})

def quiz_data_view(request,pk):
    quiz = Quiz.objects.get(pk=pk)
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




