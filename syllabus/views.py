from django.shortcuts import render, reverse
from django.views.generic import (TemplateView, DetailView,
                                  ListView, FormView, UpdateView, CreateView, DeleteView)
from .models import Level, Subname, Lecture, LectureGoals
from .forms import LectureForm, QuestionForm, AnswerForm
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from quizes.models import Quiz
from django.contrib import messages
import datetime


class LevelView(ListView):
    """
    This class view the maths level template
    :param ListView: This is to present a list of objects in level_view html page
    """
    context_object_name = 'levels'
    model = Level
    template_name = 'syllabus/level_view.html'


class SubnameView(DetailView):
    """
    This class view the maths level subject template
    :param DetailView: This is a class based generic view to present to present detail of level model in subname_view html page
    """
    context_object_name = 'levels'
    model = Level
    template_name = 'syllabus/subname_view.html'


class LectureView(DetailView):
    """
    This class view the maths level subject lectures template
    :param DetailView: This is a class based generic view to present to present detail of subject model in lecture_view html page
    """
    context_object_name = 'subnames'
    model = Subname
    template_name = 'syllabus/lecture_view.html'

    def get_context_data(self, *args, **kwargs):
        context = super(LectureView, self).get_context_data(**kwargs)
        goals = self.request.user.user_lecture_goal.all()
        user_goals = []

        for goal in goals:
            user_goals.append(goal.lecture.name)
        context['user_goals'] = user_goals
        return context

    def post(self, *args, **kwargs):
        start_date = datetime.datetime.now()

        if 'title' in self.request.POST.keys():
            lecture_id = self.request.POST['lecture-id']
            LectureGoals.objects.filter(lecture__id=lecture_id).delete()

        else:
            end_date = self.request.POST['end-date']
            lecture_id = self.request.POST['lecture-id']
            lecture = Lecture.objects.get(pk=lecture_id)

            try:
                end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
                if start_date < end_date:
                    if LectureGoals.objects.filter(lecture__id=lecture_id).count() == 0:
                        LectureGoals.objects.create(user=self.request.user, lecture=lecture, start_time=start_date,
                                                    end_time=end_date)
                else:
                    print("No old dates allowed line 66 views.py syllabus")
            except:
                print("No date chosen from the user line 68 views.py syllabus")



        return HttpResponseRedirect(reverse('syllabus:lecture_list', kwargs=self.kwargs))


class LectureDetails(DetailView, FormView):
    """
    This class view the maths level subject lecture details template
    :param DetailView: This is a class based generic view to present to present detail of lecture  in lecture_details_view html page
    :param FormView: This is a class based generic view to present to perform form check when a valid form is submitted
    """
    context_object_name = 'lectures'
    model = Lecture
    template_name = 'syllabus/lecture_details_view.html'
    form_class = QuestionForm
    second_form_class = AnswerForm

    def get_context_data(self, **kwargs):
        """
        This function adds the result to the context data with the name ‘form’,form’2,form3’
        """
        context = super(LectureDetails, self).get_context_data(**kwargs)
        context['quizes_list'] = Quiz.objects.filter(lecture_na__slug=self.kwargs['slug'])

        # for countdown
        lecture_slug = self.kwargs['slug']
        try:
            time_goals = LectureGoals.objects.get(lecture__slug=lecture_slug, user=self.request.user)
            context['time_goals'] = time_goals
        except:
            print("An exception occurred in line 90 in the views.py in the syllabus app.")

        if 'question_form' not in context:
            context['question_form'] = self.form_class
        if 'answer_form' not in context:
            context['answer_form'] = self.second_form_class

        return context

    def post(self, request, *args, **kwargs):
        """
        This function check the post request of and validation of the forms
        """
        self.object = self.get_object()
        if 'question_form' in request.POST:
            form_class = self.get_form_class()
            form_name = 'question_form'
        else:
            form_class = self.second_form_class
            form_name = 'answer_form'

        main_form = self.get_form(form_class)

        if main_form.is_valid():
            if form_name == 'question_form':
                return self.question_form_valid(main_form)
            else:
                return self.answer_form_valid(main_form)
        else:
            return HttpResponseRedirect('/')

    def get_success_url(self):
        """
        This function redirect to lecture_details when the form is successfully validated
        """
        self.object = self.get_object()
        level = self.object.level
        subname = self.object.subname

        return reverse_lazy('syllabus:lecture_details', kwargs={'level': level.slug,
                                                                'subname': subname.slug,
                                                                'slug': self.object.slug,
                                                                })

    def question_form_valid(self, form):
        self.object = self.get_object()
        f = form.save(commit=False)
        f.sender = self.request.user
        f.lecture_name = self.object.questions.name
        f.lecture_name_id = self.object.id
        f.save()
        return HttpResponseRedirect(self.get_success_url())

    def answer_form_valid(self, form):
        self.object = self.get_object()
        f = form.save(commit=False)
        f.sender = self.request.user
        f.q_name_id = self.request.POST.get('question.id')
        f.save()
        return HttpResponseRedirect(self.get_success_url())


class CreateLecture(CreateView):
    form_class = LectureForm
    context_object_name = 'subname'
    model = Subname
    template_name = 'syllabus/create_lecture.html'

    def get_success_url(self):
        self.object = self.get_object()
        level = self.object.level
        return reverse_lazy('syllabus:lecture_list', kwargs={'level': level.slug,
                                                             'slug': self.object.slug})

    def form_valid(self, form, *args, **kwargs):
        self.object = self.get_object()
        v = form.save(commit=False)
        v.user_created_lecture = self.request.user
        v.level = self.object.level
        v.subname = self.object
        v.save()
        return HttpResponseRedirect(self.get_success_url())


class UpdateLecture(UpdateView):
    fields = ('name', 'chapter', 'lecture_video', 'lecture_presentations')
    model = Lecture
    template_name = 'syllabus/update_lecture.html'
    context_object_name = 'lectures'


class DeleteLecture(DeleteView):
    model = Lecture
    context_object_name = 'lectures'
    template_name = 'syllabus/delete_lecture.html'

    def get_success_url(self):
        level = self.object.level
        subname = self.object.subname
        return reverse_lazy('syllabus:lecture_list', kwargs={'level': level.slug, 'slug': subname.slug})
