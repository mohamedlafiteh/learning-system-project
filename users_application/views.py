from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from users_application.forms import UserForm,UserProfileForm
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from syllabus.models import Level
from .models import app_user
from django.views.generic import TemplateView
from quiz.models import Assessment


# Create your views here.
def home_page(request):
    return render(request,'main_page.html')

def user_register(request):

    is_user_registered=False

    if request.method == 'POST':
        submitted_user_form=UserForm(data=request.POST)
        submitted_profile_form=UserProfileForm(data=request.POST)

        if submitted_user_form.is_valid() and submitted_profile_form.is_valid():
            user = submitted_user_form.save()
            user.save()

            profile=submitted_profile_form.save(commit=False)
            profile.user =user
            profile.save()
            is_user_registered=True
        else:
            print(submitted_user_form.errors,submitted_profile_form.errors)
    else:
        submitted_user_form=UserForm()
        submitted_profile_form=UserProfileForm()
    

    return render(request, 'users_application/user_registration.html',
                            {'is_user_registered':is_user_registered,
                             'submitted_user_form':submitted_user_form,
                             'submitted_profile_form':submitted_profile_form})

def user_account_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user_authentication = authenticate(username=username, password=password)

        if user_authentication:
            if user_authentication.is_active:
                login(request,user_authentication)
                return HttpResponseRedirect(reverse('home_page'))
            else:
                return HttpResponse("Terminated process")
        else:
            return HttpResponse("Please enter correct information")
           
    else:
        return render(request, 'users_application/user_login.html')


@login_required
def user_account_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home_page'))


class HomeView(TemplateView):
    # questions = Assessment.answer
    # if questions:
    #     template_name = 'syllabus/level_view.html'
    # else:
    #     template_name = 'users_application/home_page.html'
    template_name = 'users_application/home_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        level = Level.objects.all()
        instructor = app_user.objects.filter(app_user='instructor')
        context['levels'] = level
        context['instructor'] = instructor
        return context