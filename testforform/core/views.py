from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import Group
from django.contrib.auth.mixins import PermissionRequiredMixin
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
                if request.user.has_perm('core.view_feedback'):
                    return redirect('feedback_list_page')

        return super(LoginView, self).form_valid(form)


class RegisterView(CreateView):

    form_class = UserRegistrationForm
    template_name = "register.html"
    success_url = reverse_lazy('login_page')
    extra_context = {'form': form_class}

    def get(self, request):
        return render(request, self.template_name, self.extra_context)

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save()
            user_group = Group.objects.get(name='User')
            user.groups.add(user_group)
            user.save()
            return redirect(self.success_url)
        else:
            return render(request, self.template_name, self.extra_context)



class FeedbackWriteView(PermissionRequiredMixin, CreateView):
    form_class = FeedbackForm
    permission_required = 'core.add_feedback'
    template_name = "feedback_write.html"
    extra_context = {'form': form_class}
    model = Feedback
    success_url = reverse_lazy('login_page')

    def get(self, request):
        return render(request, self.template_name, self.extra_context)


    def post(self, request):
        form = self.form_class(request.POST, request.FILES)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = request.user
            instance.save()
            return redirect(self.success_url)
        else:
            print(form.errors)
            return render(request, self.template_name, self.extra_context)


class FeedbackListView(PermissionRequiredMixin, ListView):
    permission_required = ('core.view_feedback','core.change_feedback')
    template_name = "feedback_list.html"
    extra_context = {}

    def get(self, request):
        feedback = Feedback.objects.all()
        print(feedback)
        self.extra_context['feedbackList'] = feedback

        return render(request, self.template_name, self.extra_context)



