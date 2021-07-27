from django.shortcuts import render
from .models import Quiz
from django.http import JsonResponse
from questions.models import  Question,Answer
from results.models import  Result
from syllabus.models import Lecture
from django.db.models import Q


def Quizzes_list(request,fk):
    """
             This function for viewing the list of available quizzes
             :param fk: The lecture id
    """
    quiz = Quiz.objects.filter(lecture_na__id=fk)
    lecture = Lecture.objects.get(id=fk)
    quiz_id_obj=[]
    last_result_for_quizes=[]
    user=request.user

    for q in quiz:
        if q not in quiz_id_obj:
            quiz_id_obj.append({'id':q.id,'name':q.quiz_name,'difficulty':q.difficulty_status,'number_of_questions':q.questions_number,'required_score_to_pass':q.pass_score,'time':q.quiz_time})

    for r in quiz_id_obj:
        result = Result.objects.values_list('score',flat=True).filter(quiz__id=r['id']).filter(user__id=user.id)

        last_result = 0
        if len(result) > 0:
            last_result = result.reverse()[len(result) - 1]
            last_result_for_quizes.append({'id':r['id'],'result':last_result,'name':r['name'],'difficulty':r['difficulty'],'number_of_questions':r['number_of_questions'],'required_score_to_pass':r['required_score_to_pass'],'time':r['time']})
        else:

            last_result_for_quizes.append({'id':r['id'],'result':'no attempt','name':r['name'],'difficulty':r['difficulty'],'number_of_questions':r['number_of_questions'],'required_score_to_pass':r['required_score_to_pass'],'time':r['time']})

    return render(request,'quizes/main.html',{'obj':last_result_for_quizes, 'lecture': lecture})


# def quiz_view(request,pk):
#     """
#         This function for viewing the quiz
#         :param pk: The quiz id
#        """
#     user=request.user
#     quiz = Quiz.objects.get(pk=pk)
#     result=Result.objects.values_list('score', flat=True).filter(Q(quiz__id=pk) and Q(user__id=user.id))
#     last_result=0
#     if len(result) > 0:
#         last_result = result.reverse()[len(result) - 1]
#
#     return render(request,'quizes/quiz.html',{'obj':quiz,'result':last_result})


def quiz_detail_view(request,pk):
    """
        This function for viewing the quiz
        :param pk: The quiz id
       """
    user=request.user

    quiz = Quiz.objects.get(pk=pk)
    result=Result.objects.values_list('score', flat=True).filter(quiz__id=pk).filter(user__id=user.id)

    last_result = 0
    if len(result) > 0:
        last_result = result.reverse()[len(result) - 1]

    return render(request, 'quizes/quiz.html', {'obj': quiz, 'result': last_result})






def quiz_information(request,pk):
    """
        This function for viewing the list of available questions and options
        :param pk: The quiz id
       """
    available_quiz = Quiz.objects.get(pk=pk)
    all_questions=[]
    for question in available_quiz.get_questions():
        all_answers =[]
        for answer in question.get_answers():
            all_answers.append(answer.answer_title)
        all_questions.append({str(question):all_answers})
    return JsonResponse({
        'quizzes_data':all_questions,
        'quizzes_time':available_quiz.quiz_time,
    })

def submit_quiz(request,pk):
    """
        This function for calculating the showing results of the quiz
        :param pk: The quiz id
       """
    if request.is_ajax():
        all_questions = []
        response_data = request.POST
        result_data = dict(response_data.lists())
        result_data.pop('csrfmiddlewaretoken')
        for key in result_data.keys():
            q = Question.objects.get(question_title=key)
            all_questions.append(q)
        user = request.user
        current_quiz = Quiz.objects.get(pk=pk)
        c_score = 0
        calculator = 100 / current_quiz.questions_number
        calculator = round(calculator, 2)

        quizzes_results = []
        correct_choice = None
        for question in all_questions:
            choice = request.POST.get(str(question.question_title))
            if choice != "":
                all_answers = Answer.objects.filter(quiz_question=question)
                for ans in all_answers:
                    if choice == ans.answer_title:
                        if ans.is_correct:
                            c_score += 1
                            correct_choice = ans.answer_title
                    else:
                        if ans.is_correct:
                            correct_choice = ans.answer_title
                quizzes_results.append({str(question): {'correct_answer': correct_choice, 'answered': choice}})
            else:
                quizzes_results.append({str(question): 'not answered'})
        final_score = c_score * calculator

        Result.objects.create(quiz=current_quiz,user=user,score=final_score)

        if final_score >= current_quiz.pass_score:
            return JsonResponse({'success':True,'final_score':final_score,'quizzes_results':quizzes_results})
        else:
            return JsonResponse({'success': False,'final_score':final_score,'quizzes_results':quizzes_results})





# def Quizzes_list(request,fk):
#     """
#              This function for viewing the list of available quizzes
#              :param fk: The lecture id
#     """
#     quiz = Quiz.objects.filter(lecture_na__id=fk)
#     lecture = Lecture.objects.get(id=fk)
#     quiz_id_obj=[]
#     last_result_for_quizes=[]
#
#
#     for q in quiz:
#         if q not in quiz_id_obj:
#             quiz_id_obj.append({'id':q.id,'name':q.quiz_name,'difficulty':q.difficulty_status,'number_of_questions':q.questions_number,'required_score_to_pass':q.pass_score,'time':q.quiz_time})
#
#     user = request.user
#
#     quiz_id=None
#     last_result = None
#
#     quiz_id = Result.objects.values_list('quiz_id', flat=True).filter(user__id=user.id)
#
#     q_ids=[]
#     if len(quiz_id) > 0:
#         for id in quiz_id:
#             if id not in q_ids:
#                 q_ids.append(id)
#
#     for r in quiz_id_obj:
#         if r['id'] in q_ids:
#             result = Result.objects.values_list('score', flat=True).filter(user__id= user.id)
#             # result = Result.objects.values_list('score', flat=True).filter(Q(quiz__id= r['id']) and Q(user__id=user.id))
#             last_result = result.reverse()[len(result) - 1]
#
#
#             last_result_for_quizes.append(
#                 {'id': r['id'], 'result': last_result, 'name': r['name'], 'difficulty': r['difficulty'],
#                  'number_of_questions': r['number_of_questions'],
#                  'required_score_to_pass': r['required_score_to_pass'], 'time': r['time']})
#         else:
#
#             last_result_for_quizes.append(
#                 {'id': r['id'], 'result': 'no attempt', 'name': r['name'], 'difficulty': r['difficulty'],
#                  'number_of_questions': r['number_of_questions'],
#                  'required_score_to_pass': r['required_score_to_pass'], 'time': r['time']})
#     return render(request,'quizes/main.html',{'obj':last_result_for_quizes, 'lecture': lecture})


# def quiz_detail_view(request,pk):
#     """
#         This function for viewing the quiz
#         :param pk: The quiz id
#        """
#     quiz = Quiz.objects.get(pk=pk)
#     user = request.user
#
#     result=Result.objects.values_list('score', flat=True).filter(quiz__id=pk)
#     # result = Result.objects.values_list('score', flat=True).filter(Q(quiz__id=pk) and Q(user__id=user.id))
#
#     last_result=0
#
#     if len(result) > 0:
#         last_result = result.reverse()[len(result) - 1]
#
#     return render(request,'quizes/quiz.html',{'obj':quiz,'result':last_result})


# def quiz_information(request,pk):
#     """
#         This function for viewing the list of available questions and options
#         :param pk: The quiz id
#        """
#     available_quiz = Quiz.objects.get(pk=pk)
#     all_questions=[]
#     for question in available_quiz.get_questions():
#         all_answers =[]
#         for answer in question.get_answers():
#             all_answers.append(answer.answer_title)
#         all_questions.append({str(question):all_answers})
#     return JsonResponse({
#         'quizzes_data':all_questions,
#         'quizzes_time':available_quiz.quiz_time,
#     })

# def submit_quiz(request,pk):
#     """
#         This function for calculating the showing results of the quiz
#         :param pk: The quiz id
#        """
    # if request.is_ajax():
    #     all_questions =[]
    #     response_data = request.POST
    #     result_data = dict(response_data.lists())
    #     result_data.pop('csrfmiddlewaretoken')
    #     for key in result_data.keys():
    #         q = Question.objects.get(question_title=key)
    #         all_questions.append(q)
    #     user = request.user
    #     current_quiz = Quiz.objects.get(pk=pk)
    #     c_score =0
    #     calculator= 100 /current_quiz.questions_number
    #     calculator=round(calculator, 2)
    #
    #     quizzes_results =[]
    #     correct_choice=None

        # for question in all_questions:
        #     choice = request.POST.get(str(question.question_title))
        #     if choice !="":
        #         all_answers = Answer.objects.filter(quiz_question=question)
        #         for ans in all_answers:
        #             if choice == ans.answer_title:
        #                 if ans.is_correct:
        #                     c_score+=1
        #                     correct_choice=ans.answer_title
        #             else:
        #                 if ans.is_correct:
        #                     correct_choice=ans.answer_title
        #         quizzes_results.append({str(question):{'correct_answer':correct_choice,'answered':choice}})
        #     else:
        #         quizzes_results.append({str(question):'not answered'})
        # final_score=c_score*calculator

        # Result.objects.create(quiz=current_quiz,user=user,score=final_score)
        #
        # if final_score >= current_quiz.pass_score:
        #     return JsonResponse({'success':True,'final_score':final_score,'quizzes_results':quizzes_results})
        # else:
        #     return JsonResponse({'success': False,'final_score':final_score,'quizzes_results':quizzes_results})
        #
        #

