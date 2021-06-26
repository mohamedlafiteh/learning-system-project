from django import forms
from .models import Lecture,Question,Answer,Quizes


class LectureForm(forms.ModelForm):
    class Meta:
        model = Lecture
        fields = ('lecture_id','name','chapter','lecture_video','lecture_presentations')

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('question_body',)

        labels = {"body":"Question:"}

        widgets = {
            'question_body': forms.Textarea(attrs={'class':'form-control', 'rows':4, 'cols':70, 'placeholder':"Write a question."}),
        }


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ('answer_body',)

        widgets = {
            'answer_body': forms.Textarea(attrs={'class':'form-control', 'rows':2, 'cols':10}),
        }


class QuizAnswerForm(forms.ModelForm):
    class Meta:
        model = Quizes
        fields = '__all__'


        widgets = {
            'answer_body': forms.Textarea(attrs={'class':'form-control', 'rows':2, 'cols':10}),
        }


