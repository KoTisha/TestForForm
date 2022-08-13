from email import message
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, FormView
from django.views.generic.base import View
from .models import Feedback
from .forms import FeedbackForm, UserRegistrationForm, UserLoginForm


# Create your views here.

class LogoutView(View):
    success_url = reverse_lazy('login_page')
    def get(self, request):
        logout(request)
        return redirect('login_page')
class LoginView(FormView):
    form_class = UserLoginForm
    template_name = "login.html"
    success_url = reverse_lazy('feedback_write_page')
    extra_context = {'form': form_class}

    def get(self, request):
        return render(request, self.template_name, self.extra_context)

    def post(self, request):
        form = self.form_class(request, data=request.POST)

        if form.is_valid():
            user = authenticate(self.request, username=self.request.POST['username'], password=self.request.POST['password'])
            if user is not None:
                login(request, form.get_user())


        return super(LoginView, self).form_valid(form)


class RegisterView(CreateView):

    form_class = UserRegistrationForm
    template_name = "register.html"
    success_url = reverse_lazy('feedback_write_page')
    extra_context = {'form': form_class}


    def get(self, request):
        # if request.method == "POST":
        #     form = UserRegistrationForm(request.POST)
        #     if form.is_valid():
        #         new_user = form.save()
        #         self.extra_context = {'new_user': new_user}
        # form = UserRegistrationForm()
        # self.extra_context = {'form': form}
        return render(request, self.template_name, self.extra_context)

    def form_validate(self, form):
        form.save()
        return super(RegisterView, self).form_valid(form)


class FeedbackWriteView(CreateView):
    template_name = "feedback_write.html"

    def get(self, request):
        return render(request, self.template_name, self.extra_context)

class FeedbackListView(ListView):
    template_name = "feedback_list.html"

    def get(self, request):
        return render(request, self.template_name, self.extra_context)



