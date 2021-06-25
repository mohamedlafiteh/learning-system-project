from django.shortcuts import render
from django.views.generic import (TemplateView, DetailView,
                                    ListView, CreateView,
                                    UpdateView,DeleteView,FormView,)
from .models import Assessment,Result
from django.urls import reverse_lazy
from .forms import AssessmentForm
from django.http import HttpResponseRedirect
import re

# Create your views here.
def Assessmentview(request):
    questions = Assessment.objects.all()

    if request.method == 'POST':
        answers = []
        data = request.POST
        data_ = dict(data.lists())
        data_.pop('csrfmiddlewaretoken')
        n=0
        for k,v in data_.items():
            nn = re.sub("\D", "", v[n])
            answers.append(nn)
            n+1

        strings = [str(integer) for integer in answers]
        numbers_answered=[]

        for num in range(0,len(strings)-1):
            n= re.sub("\D", "", strings[num])
            numbers_answered.append(int(n))
        score = 0
        multiplier = 100 / 4
        results = []
        question_answers = Assessment.objects.values('answer')
        correct_a_list_values_from_model= []
        correct_l = []
        for v in question_answers:
            question_answers_value = Assessment.objects.values(v.get('answer').lower())
            l = [integer for integer in question_answers_value]
            correct_a_list_values_from_model.append(l)
        for v in correct_a_list_values_from_model[0]:
            for key, value in v.items():
                correct_l.append(int(value))

        # compare answers with the correct answers list
        for a in numbers_answered:
            if a in correct_l:
                score +1

        final= score * multiplier
        print(final)


                #
                # print(question_answers)
                #

                # for a in question_answers:
                #     if a_selected == a.text:
                #         if a.correct:
                #             score += 1
                #             correct_answer = a.text
                #     else:
                #         if a.correct:
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

