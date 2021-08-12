
from django.urls import path
from . import views

app_name = 'syllabus'

urlpatterns = [
    # path('',views.LevelView.as_view(),name='level_list'),
    path('lectures/',views.LectureView.as_view(),name='lecture_list'),
    # path('<slug:slug>/',views.SubnameView.as_view(),name='subname_list'),
    # path('<str:level>/<slug:slug>/',views.LectureView.as_view(),name='lecture_list'),
    path('lectures/create/',views.CreateLecture.as_view(),name='create_lecture'),
    path('lectures/<slug:slug>/',views.LectureDetails.as_view(),name='lecture_details'),
    path('<slug:slug>/update/',views.UpdateLecture.as_view(),name='lecture_update'),
    path('<slug:slug>/delete/',views.DeleteLecture.as_view(),name='lecture_delete'),
]