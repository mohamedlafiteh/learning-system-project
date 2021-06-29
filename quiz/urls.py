
from django.urls import path
from .views import Assessmentview,quiz_view,quiz_data_view,save_quiz_view

app_name = 'quiz'

# urlpatterns = [
#     path('',views.Assessmentview,name='assess_list'),
#     path('quiz/', views.Assessmentview, name='result_list'),
#
# ]

urlpatterns = [
    path('', Assessmentview,name='assess_list'),
    path('get/<int:pk>',quiz_view,name='quiz-view'),
    path('<pk>/save/', save_quiz_view, name='save-view'),
    path('<pk>/data/', quiz_data_view, name='quiz-data-view'),

]