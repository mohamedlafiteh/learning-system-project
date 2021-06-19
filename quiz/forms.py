
from django import forms
from .models import Assessment

class AssessmentForm(forms.ModelForm):
    class Meta:
        model=Assessment
        fields=['mark','question','option1','option2','option3','answer']
        widgets = {
            'question': forms.Textarea(attrs={'rows': 3, 'cols': 50})
        }
