from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from users_application.forms import UserForm,UserProfileForm
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
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