from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt
urlpatterns = [
    path('register', views.register.as_view(), name='register'),
    path('login', views.userLogin.as_view(), name='login'),
    path('logout', views.Logout.as_view(), name='logout'),
    path('username-check', csrf_exempt(views.UsernameCheck.as_view())),
    path('email-check', csrf_exempt(views.EmailCheck.as_view())),
    path('activate/<uidb64>/<token>', views.Verification.as_view(), name='activate'),
    path('forgate-password', views.ForgatePassword.as_view(), name='forgate_password'),
    path('reset-password/<uidb64>/<token>', views.ResetPassword.as_view(), name='reset_password'),
    path('preferences', views.Preferences.as_view(), name='preferences'),
]
