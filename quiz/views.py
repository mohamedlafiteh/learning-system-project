from django.shortcuts import render
from .models import Assessment,Results

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


        numbers_answered = []
        counter_n=0
        for num in range(0,len(strings)):
            n= re.sub("\D", "", strings[num])
            counter_n=counter_n+1
            try:
                numbers_answered.append(int(n))
            except:
                print("It is not number the last value line 42 in view .py quiz app")

        question_answers = Assessment.objects.values('answer')
        correct_a_list_values_from_model= []
        correct_l = []

        for v in question_answers:
            question_answers_value = Assessment.objects.values(v.get('answer').lower())
            print(question_answers_value)

            l = [integer for integer in question_answers_value]
            correct_a_list_values_from_model.append(l)


        for v in correct_a_list_values_from_model[0]:
            for key, value in v.items():
                if value.isnumeric():
                    correct_l.append(int(value))

        # compare answers with the correct answers list
        score = 0
        multiplier = 100 / 5

        for a in numbers_answered:

             if a in correct_l:
                 score=score+1

        final= score * multiplier

        user = request.user
        Results.objects.create(learner=user, mark=final)

        assess_result=Results.objects.values_list('mark', flat=True).filter(learner__id=user.id)
        last_results=assess_result.reverse()[len(assess_result)-1]

        return render(request, 'quiz/results_view.html', {'results': last_results})
    else:
        return render(request, 'quiz/assessment_view.html', {'questions': questions})

