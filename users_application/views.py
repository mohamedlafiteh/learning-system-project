from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from users_application.forms import UserForm,UserProfileForm
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from syllabus.models import Level
from .models import app_user
from django.views.generic import TemplateView
from quiz.models import Result


# Create your views here.
#This function for the home page
def home_page(request):
    return render(request,'main_page.html')

#This function for the about page
def about_page(request):
    return render(request,'users_application/about_page.html')

#This function for the user regstraion page
def user_register(request):

    is_user_registered=False
    #Checking if the request is POST
    if request.method == 'POST':
        submitted_user_form=UserForm(data=request.POST)
        submitted_profile_form=UserProfileForm(data=request.POST)

        if submitted_user_form.is_valid() and submitted_profile_form.is_valid():
            user = submitted_user_form.save()
            user.save()

            user_profile=submitted_profile_form.save(commit=False)
            user_profile.user =user
            user_profile.save()
            is_user_registered=True
        else:
            print("error in register forms")
    else:
        submitted_user_form=UserForm()
        submitted_profile_form=UserProfileForm()
    

    return render(request, 'users_application/user_registration.html',
                            {'is_user_registered':is_user_registered,
                             'submitted_user_form':submitted_user_form,
                             'submitted_profile_form':submitted_profile_form})
#Loging function
def user_account_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        #Validate the user
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

#Home page view after assessment attempt
class mainPageView(TemplateView):
    template_name = 'users_application/home_page.html'

    def get_context_data(self, **kwargs):
        user=self.request.user
        assess_result = Result.objects.values_list('score', flat=True).filter(user__id=user.id).last()

        context = super().get_context_data(**kwargs)
        level = Level.objects.all()
        instructor = app_user.objects.filter(app_user='instructor')

        context['result']=assess_result
        context['levels'] = level
        context['instructor'] = instructor
        return context