from django import forms
from django.contrib.auth.models import User
from users_application.models import app_user
from django.contrib.auth.forms import UserCreationForm


class UserForm(UserCreationForm):
    email = forms.EmailField()

    class Meta():
        model = User
        fields = ('username','first_name','last_name', 'email','password1','password2')

        labels = {
        'password1':'Password',
        'password2':'Password Confirmation'
        }


class UserProfileForm(forms.ModelForm):
    instructor = 'instructor'
    learner = 'learner'
   
    types_of_users = [
        (learner, 'learner'),]

    user_type = forms.ChoiceField(required=True, choices=types_of_users)

    class Meta():
        model = app_user
        fields = ('user_type',)