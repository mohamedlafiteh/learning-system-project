from django.shortcuts import render
from django.views.generic import (TemplateView, DetailView,
                                  ListView, FormView, UpdateView, CreateView, DeleteView)
from .models import Level, Subname, Lecture,Quizes
from .forms import LectureForm, QuestionForm, AnswerForm,QuizAnswerForm
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy



class LevelView(ListView):
    context_object_name = 'levels'
    model = Level
    template_name = 'syllabus/level_view.html'


class SubnameView(DetailView):
    context_object_name = 'levels'
    model = Level
    template_name = 'syllabus/subname_view.html'


class LectureView(DetailView):
    context_object_name = 'subnames'
    model = Subname
    template_name = 'syllabus/lecture_view.html'


class LectureDetails(DetailView, FormView):
    context_object_name = 'lectures'
    model = Lecture
    template_name = 'syllabus/lecture_details_view.html'
    form_class = QuestionForm
    second_form_class = AnswerForm
    form_class_quiz = QuizAnswerForm

    def get_context_data(self, **kwargs):
        context = super(LectureDetails, self).get_context_data(**kwargs)
        context['quizes_list'] = Quizes.objects.all()

        if 'form' not in context:
            context['form'] = self.form_class
        if 'form2' not in context:
            context['form2'] = self.second_form_class
        if 'form3' not in context:
            context['form3'] = self.form_class_quiz
        return context


    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if 'form' in request.POST:
            form_class = self.get_form_class()
            form_name = 'form'
        elif 'form2' in request.POST:
            form_class = self.second_form_class
            form_name = 'form2'
        else:
            form_class = self.form_class_quiz
            form_name = 'form3'

        form = self.get_form(form_class)
        if form.is_valid():
            if form_name == 'form':
                print("Question form returned")
                return self.form_valid(form)
            elif form_name == 'form2':
                print("Answer form returned")
                return self.form2_valid(form)
            else:
                print(form)
                return self.form3_valid(form)
        else:
            return HttpResponseRedirect('/')



    def get_success_url(self):
        self.object = self.get_object()
        level = self.object.level
        subname = self.object.subname
        return reverse_lazy('syllabus:lecture_details', kwargs={'level': level.slug,
                                                                'subname': subname.slug,
                                                                'slug': self.object.slug})

    def form_valid(self, form):
        self.object = self.get_object()
        f = form.save(commit=False)
        f.sender = self.request.user
        f.lecture_name = self.object.questions.name
        f.lecture_name_id = self.object.id
        f.save()
        return HttpResponseRedirect(self.get_success_url())

    def form2_valid(self, form):
        self.object = self.get_object()
        f = form.save(commit=False)
        f.sender = self.request.user
        f.q_name_id = self.request.POST.get('question.id')
        f.save()
        return HttpResponseRedirect(self.get_success_url())

    def form3_valid(self, form):
        self.object = self.get_object()
        f = form.save(commit=False)
        f.sender = self.request.user
        f.lecture_name_id = self.object.id
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
    fields = ('name', 'chapter', 'lecture_video', 'lecture_presentations', 'lecture_notes')
    model = Lecture
    template_name = 'syllabus/update_lecture.html'
    context_object_name = 'lectures'


class DeleteLecture(DeleteView):
    model = Lecture
    context_object_name = 'lectures'
    template_name = 'syllabus/delete_lecture.html'

    def get_success_url(self):
        print(self.object)
        level = self.object.level
        subname = self.object.subname
        return reverse_lazy('syllabus:lecture_list', kwargs={'level': level.slug, 'slug': subname.slug})
