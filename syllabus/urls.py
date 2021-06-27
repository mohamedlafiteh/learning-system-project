
from django.urls import path
from . import views

app_name = 'syllabus'

urlpatterns = [
    path('',views.LevelView.as_view(),name='level_list'),
    path('<slug:slug>/',views.SubnameView.as_view(),name='subname_list'),
    # path('add-goal/', views.setGoal,name="set-goal"),
    path('<str:level>/<slug:slug>/',views.LectureView.as_view(),name='lecture_list'),
    path('<str:level>/<str:slug>/create/',views.CreateLecture.as_view(),name='create_lecture'),
    path('<str:level>/<str:subname>/<slug:slug>/',views.LectureDetails.as_view(),name='lecture_details'),
    path('<str:level>/<str:subname>/<slug:slug>/update/',views.UpdateLecture.as_view(),name='lecture_update'),
    path('<str:level>/<str:subname>/<slug:slug>/delete/',views.DeleteLecture.as_view(),name='lecture_delete'),
]