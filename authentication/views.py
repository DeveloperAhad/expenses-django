from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.views.generic import View
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import EmailMessage
from django.contrib import auth
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.conf import settings
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

import threading


from .models import UserPreference

from validate_email import validate_email
from .utils import account_tokens_genetator, password_tokens_genetator

import json
import os

# Create your views here.
class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)
    
    def run(self):
        self.email.send(fail_silently=False)

class userLogin(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'authentication/login.html'); 
        return redirect('expenses')

    def post(self, request):

        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password:
            user = auth.authenticate(username=username, password=password)

            if user:
                if user.is_active:
                    auth.login(request, user)
                    messages.success(request, 'Welcome ' + user.username + ' you are now login!')
                    return redirect('expenses')
                messages.error(request, 'Account is not active, please check your email')
                return redirect('login')

            messages.error(request, 'Invalid credentials, try again!')
            return redirect('login')

        messages.error(request, 'field must not be empty!')
        return render(request, 'authentication/login.html'); 

class register(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'authentication/register.html');
        
        return redirect('expenses')

    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        context = {
            'fileValues': request.POST
        }

        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password) < 6:
                    messages.error(request, 'Password is too short!')
                    return render(request, 'authentication/register.html', context); 
                user = User.objects.create_user(username=username, email=email)
                user.set_password(password)
                user.is_active = False
                user.save()

                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                
                domain = get_current_site(request).domain
                link= reverse('activate', kwargs={'uidb64':uidb64, 'token': account_tokens_genetator.make_token(user)})
                active_url = 'http://'+domain+link

                print(active_url)

                email_subject = 'Active your account'
                email_body = f'Hi {user.username},\nPlease use this link for active your account.\n{active_url}';

                email = EmailMessage(email_subject, email_body,
                    'Money Management <noreply@moneymanagment.com>',
                    [email],
                )
                EmailThread(email).start()

                messages.success(request, 'Account create successfully!')
                return render(request, 'authentication/register.html');

        messages.error(request, 'Account not created')
        return render(request, 'authentication/register.html');

class Verification(View):
    def get(self, request, uidb64, token):
        try: 
            id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            if not account_tokens_genetator.check_token(user, token):
                messages.warning(request, 'User already activated!')
                redirect('login'+'?message='+'User already activated!')

            if user.is_active:
                return redirect('login') 
            
            user.is_active = True
            user.save()
            messages.success(request, 'Account activate successfully!')
            return redirect('login')

        except Exception as ex:
            pass

        return redirect('login');


class UsernameCheck(View):    
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']
        if not str(username).isalnum():
            return JsonResponse({"username_error": "username should be user alphanumeric character"}, status=400)
        
        if User.objects.filter(username=username).exists():
            return JsonResponse({"username_error": "username already exists choice another one!"}, status=409)
        
        return JsonResponse({"username_valid": True})

class ForgatePassword(View):
    def get(self, request):
        return render(request, 'authentication/reset-password.html')

    def post(self, request):
        email = request.POST.get('email')
        is_user = User.objects.filter(email=email).exists()
        if is_user:
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            domain = get_current_site(request).domain
            link= reverse('reset_password', kwargs={'uidb64':uidb64, 'token': password_tokens_genetator.make_token(user)})
            active_url = 'http://'+domain+link
            print(active_url)
            email_subject = 'Active your account'
            email_body = f'Hi {user.username},\nPlease use this link for reset your password.\n{active_url}';
            email = EmailMessage(email_subject, email_body,
                    'Money Management <topfunfactory@gmail.com>',
                    [email],
                )
            EmailThread(email).start()
            messages.success(request, 'Check your email for rest your password')
            return render(request, 'authentication/reset-password.html')
        
        messages.error(request, 'There was no user in this email address!')
        return render(request, 'authentication/reset-password.html')

class ResetPassword(View):
    def get(self, request, uidb64, token):
        context = {
            'uidb64': uidb64,
            'token': token
        }
        try: 
            user_id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
            print(password_tokens_genetator.check_token(user, token))

            if not password_tokens_genetator.check_token(user, token):
                messages.info(request, 'Password link is invalid, please request a new one')
                return redirect('forgate_password')

        except Exception as ex:
            messages.info(request, 'Password link is invalid, please request a new one')
            return redirect('forgate_password')

        return render(request, 'authentication/set-newpassword.html', context)

    def post(self, request, uidb64, token):
        context = {
            'uidb64': uidb64,
            'token': token
        }

        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password != password2:
            messages.error(request, 'Password do not match!')
            return render(request, 'authentication/set-newpassword.html', context)
        
        if len(password) < 6:
            messages.error(request, 'Password is too short!')
            return render(request, 'authentication/set-newpassword.html', context)
        
        try: 
            user_id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successfully, you can login with your new password')
            return redirect('login')
        except Exception as ex:
            messages.error(request, 'Somthing wrong try again!')
            return render(request, 'authentication/set-newpassword.html', context)

class EmailCheck(View):    
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']
        if not validate_email(email):
            return JsonResponse({"email_error": "Email address is not valid!"}, status=400)
        
        if User.objects.filter(email=email).exists():
            return JsonResponse({"email_error": "Email already exists choice another one!"}, status=409)
        
        return JsonResponse({"email_valid": True})


class Logout(View):
    def post(self, request):
        auth.logout(request)
        messages.info(request, 'Logout successfully!')
        return redirect('login')


class Preferences(View):
    current_data = []

    @method_decorator(login_required(login_url='login'))
    def dispatch(self, *args, **kwargs):
        return super(Preferences, self).dispatch(*args, **kwargs)

    def currency(self):
        file_path = os.path.join(settings.BASE_DIR, 'currencies.json')
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
            for k,v in data.items():
                self.current_data.append({'name':v,'value':k})


    def get(self, request):
        self.currency()
        selected_currency = ''
        find_user_currency = UserPreference.objects.filter(user=request.user).exists()
        if find_user_currency:
            get_currency = UserPreference.objects.get(user=request.user)
            selected_currency = get_currency.currency.split('-')[1]
            
        context = {
            'currencies': self.current_data,
            'selected_currency':selected_currency
        }
        return render(request, 'preferences/index.html', context)


    def post(self, request):
        self.currency()
        get_currency = request.POST.get('currencie')
        currency_list = get_currency.split('-')
        valid_currency = False

        for x in self.current_data:
            if currency_list[0] == x['value'] and currency_list[1] == x['name']:
                valid_currency = True
                break;

        if valid_currency: 
            find_user_currency = UserPreference.objects.filter(user=request.user).exists()
            if find_user_currency:
                change_currency = UserPreference.objects.get(user=request.user)
                change_currency.currency = get_currency
                change_currency.save()
            else:
                make_currency = UserPreference.objects.create(user=request.user, currency=get_currency);
                make_currency.save()
            messages.success(request, 'Currency select successfully!')
            return redirect('preferences')
        
        return render(request, 'preferences/index.html', {'currencies': self.current_data})
