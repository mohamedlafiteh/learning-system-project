from django.urls import path
from .views import QuizListView,quiz_view,quiz_data_view,save_quiz_view,select_quiz_view

app_name ='quizes'

urlpatterns = [
    path('', QuizListView.as_view(),name='main-view'),
    path('select/<fk>/', select_quiz_view, name='select_quiz_view'),
    path('select/<lecture_id>/<quiz_id>/',quiz_view,name='quiz-view'),
    path('<pk>/save/', save_quiz_view, name='save-view'),
    path('<pk>/data/', quiz_data_view, name='quiz-data-view'),

]
