from django.core.mail import EmailMessage
from django.contrib import messages
from django.utils import timezone
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import Group
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, FormView
from django.views.generic.base import View
from .models import Feedback, SubmitUser
from .forms import *


# Create your views here.

class LogoutView(View):
    success_url = reverse_lazy('login_page')
    def get(self, request):
        logout(request)
        messages.success(request, 'Успешный выход!')
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
                messages.success(request, 'Залогинено!')
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
            messages.success(request, 'Реристрация прошла успешно!')
            return redirect(self.success_url)
        else:
            messages.error(request, 'Форма неверна')
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
        submittingUser = SubmitUser.objects.get(user = request.user.id)
        try:
            timeDifference = timezone.now() - submittingUser.lastSubmitDate
            timeDifference = timeDifference.total_seconds()
        except:
            timeDifference = 86401

        if timeDifference > 1:
            if form.is_valid():
                send_email(request)
                savingForm = form.save(commit=False)
                savingForm.author = request.user
                savingForm.save()
                SubmitUser.objects.filter(user=request.user.id).update(lastSubmitDate=timezone.now())
                messages.success(request, 'Сохранено!')
                return render(request, self.template_name, self.extra_context)
            else:
                messages.error(request, 'Форма неверна')
                return render(request, self.template_name, self.extra_context)
        else:
            messages.error(request, 'Вы уже оставляли сегодня сообщение')
            return render(request, self.template_name, self.extra_context)


class FeedbackListView(PermissionRequiredMixin, ListView):
    form_class = FeedbackCheckForm
    permission_required = ('core.view_feedback','core.change_feedback')
    template_name = "feedback_list.html"
    extra_context = {
        'form': form_class,
        'feedbackList': Feedback.objects.all(),
        }
    success_url = reverse_lazy('login_page')
    feedback = {}

    def get(self, request):
        return render(request, self.template_name, self.extra_context)

    def post(self, request):
        for feedback in self.extra_context['feedbackList']:
            buttonName = str(feedback.id) + '_button'
            if buttonName in request.POST:
                form = self.form_class(request.POST, instance=feedback)

                if form.is_valid():
                    savingForm = form.save(commit=False)
                    savingForm.save()

                    messages.success(request, 'Сохранено!')
                    return render(request, self.template_name, self.extra_context)

        messages.error(request, 'Не удалось')


def send_email(request):
    messages.success(request, "начата функция")
    message = request.POST['message'] + ' from: ' + request.user.email
    email = EmailMessage(
        request.POST['title'],
        message,
        'admin@example.com',
        ['admin@example.com'],
    )
    if request.FILES:
        try:
            attachingFile = request.FILES['file']
            email.attach(attachingFile.name, attachingFile.read(),attachingFile.content_type)
            messages.success(request, "файлы успешно прикреплены")
        except:
            return "Attachment error"
    email.send()
    messages.success(request, "письмо отправлено!")
    return "OK!"