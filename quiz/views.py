# from django.shortcuts import render
# from django.views.generic import (TemplateView, DetailView,
#                                     ListView, CreateView,
#                                     UpdateView,DeleteView,FormView,)
# from .models import Assessment
# from django.urls import reverse_lazy
# from .forms import AssessmentForm
# from django.http import HttpResponseRedirect
#
# # Create your views here.
# def Assessmentview(request):
#     questions = Assessment.objects.all()
#     if request.method == 'POST':
#         results = request.POST.items()
#         # for key, value in request.POST.items():
#         return render(request, 'quiz/results_view.html', {'results': results})
#     else:  # GET
#         return render(request, 'quiz/assessment_view.html', {'questions': questions})
#
