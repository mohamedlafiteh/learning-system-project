from django.urls import path
from .views import Quizzes_list,quiz_detail_view,quiz_information,submit_quiz

app_name ='quizes'

urlpatterns = [
    path('<int:fk>', Quizzes_list,name='main-view'),
    path('get/<int:pk>',quiz_detail_view,name='quiz-detail-view'),
    path('<pk>/save/', submit_quiz, name='submit-view'),
    path('<pk>/data/', quiz_information, name='quiz-information'),

]