from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import FormView
from .models import Feedback

# Create your views here.

class LoginView(FormView):
    pass

class FeedbackWriteView(FormView):
    pass

class FeedbackListView(ListView):
    pass



