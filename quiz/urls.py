
from django.urls import path
from .views import Assessmentview,available_quiz_view,quiz_detail_view,submit_quiz

app_name = 'quiz'

# urlpatterns = [
#     path('',views.Assessmentview,name='assess_list'),
#     path('quiz/', views.Assessmentview, name='result_list'),
#
# ]

urlpatterns = [
    path('', Assessmentview,name='assess_list'),
    path('get/<int:pk>',available_quiz_view,name='quiz-view'),
    path('<pk>/save/', submit_quiz, name='save-view'),
    path('<pk>/data/', quiz_detail_view, name='quiz-data-view'),

]