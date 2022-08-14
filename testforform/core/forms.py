from django import forms
from .models import Feedback
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')


class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ('title', 'message', 'file', )
