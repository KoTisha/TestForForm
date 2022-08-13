from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('', RedirectView.as_view(url='/login')),
    path('feedback/', views.FeedbackWriteView.as_view(), name='feedback_write_page'),
    path('feedback_list/', views.FeedbackListView.as_view(), name='feedback_list_page'),
    path('login/', views.LoginView.as_view(), name='login_page'),
    path('register/', views.RegisterView.as_view(), name='register_page'),
    path('logout/', views.LogoutView.as_view(), name='logout_page'),
]
