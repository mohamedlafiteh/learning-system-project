from django.shortcuts import render
from django.views.generic import (TemplateView, DetailView,
                                    ListView, CreateView,
                                    UpdateView,DeleteView,FormView,)
from .models import Assessment
from django.urls import reverse_lazy
from .forms import AssessmentForm
from django.http import HttpResponseRedirect

# Create your views here.
def Assessmentview(request):
    questions = Assessment.objects.all()

    # if request.method == 'POST':
    #     results = request.POST.items()
    #     # for key, value in request.POST.items():
    #     #     print(value)
    #     return render(request, 'quiz/results_view.html', {'results': results})
    # else:  # GET
    #     return render(request, 'quiz/assessment_view.html', {'questions': questions})

    if request.method == 'POST':
        questions = []
        data = request.POST
        data_ = dict(data.lists())
        data_.pop('csrfmiddlewaretoken')
        for k in data_.keys():
            question = Assessment.objects.get(id=k)
            questions.append(question)
            print(str(question))
        return render(request, 'quiz/results_view.html', {'results': data_})
    else:
        return render(request, 'quiz/assessment_view.html', {'questions': questions})
    # data_.pop('csrfmiddlewaretoken')
    # for k in data_.keys():
    #     question = Question.objects.get(text=k)
    #     questions.append(question)
    # user = request.user
    # quiz = Quiz.objects.get(pk=pk)
    # score = 0
    # multiplier = 100 / quiz.number_of_questions
    # results = []
    # correct_answer = None
    #
    # for q in questions:
    #     a_selected = request.POST.get(str(q.text))
    #     if a_selected != "":
    #         question_answers = Answer.objects.filter(question=q)
    #         for a in question_answers:
    #             if a_selected == a.text:
    #                 if a.correct:
    #                     score += 1
    #                     correct_answer = a.text
    #             else:
    #                 if a.correct:
    #                     correct_answer = a.text
    #         results.append({str(q): {'correct_answer': correct_answer, 'answered': a_selected}})
    #     else:
    #         results.append({str(q): 'not answered'})
    # score_ = score * multiplier
    # Result.objects.create(quiz=quiz, user=user, score=score_)
    # if score_ >= quiz.required_score_to_pass:
    #     return JsonResponse({'passed': True, 'score': score_, 'results': results})
    # else:
    #     return JsonResponse({'passed': False, 'score': score_, 'results': results})
    #

