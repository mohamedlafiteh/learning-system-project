from django.shortcuts import render
from .models import Quiz
from django.http import JsonResponse
from questions.models import  Question,Answer
from results.models import  Result
from syllabus.models import Lecture


def QuizListView(request,fk):
    """
             This function for viewing the list of available quizzes
             :param fk: The lecture id
    """
    quiz = Quiz.objects.filter(lecture_na__id=fk)
    lecture = Lecture.objects.get(id=fk)
    quiz_id_obj=[]
    last_result_for_quizes=[]

    for q in quiz:
        if q not in quiz_id_obj:
            quiz_id_obj.append({'id':q.id,'name':q.name,'difficulty':q.difficulty,'number_of_questions':q.number_of_questions,'required_score_to_pass':q.required_score_to_pass,'time':q.time})

    for r in quiz_id_obj:
        result = Result.objects.values_list('score', flat=True).filter(quiz__id=r['id'])
        last_result = 0
        if len(result) > 0:
            last_result = result.reverse()[len(result) - 1]
            last_result_for_quizes.append({'id':r['id'],'result':last_result,'name':r['name'],'difficulty':r['difficulty'],'number_of_questions':r['number_of_questions'],'required_score_to_pass':r['required_score_to_pass'],'time':r['time']})
        else:
            last_result_for_quizes.append({'id':r['id'],'result':'no attempt','name':r['name'],'difficulty':r['difficulty'],'number_of_questions':r['number_of_questions'],'required_score_to_pass':r['required_score_to_pass'],'time':r['time']})

    return render(request,'quizes/main.html',{'obj':last_result_for_quizes, 'lecture': lecture})


def quiz_view(request,pk):
    """
        This function for viewing the quiz
        :param pk: The quiz id
       """
    quiz = Quiz.objects.get(pk=pk)
    result=Result.objects.values_list('score', flat=True).filter(quiz__id=pk)
    last_result=0
    if len(result) > 0:
        last_result = result.reverse()[len(result) - 1]

    return render(request,'quizes/quiz.html',{'obj':quiz,'result':last_result})


def quiz_data_view(request,pk):
    """
        This function for viewing the list of available questions and options
        :param pk: The quiz id
       """
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
    """
        This function for calculating the showing results of the quiz
        :param pk: The quiz id
       """
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




