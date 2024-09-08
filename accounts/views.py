from .models import Profile
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login , logout
from django.http import HttpResponseRedirect, HttpResponse

def login_page(request):
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Check if the user already exists
        user_obj = User.objects.filter(username=email)
        
        if not user_obj.exists():
            messages.success(request, "Account not Found.")
            return HttpResponseRedirect(request.path_info)
        if not user_obj[0].profile.is_email_verified:
            messages.warning(request, "Your account is not verified.")
            return HttpResponseRedirect(request.path_info)
            
        
        
        # Login form
        user_obj = authenticate(usernme = email , password = password )
        if user_obj:
            login(request , user_obj)
            return redirect('/')
        
        messages.warning(request, "Invalid Credentials.")
        return HttpResponseRedirect(request.path_info)
        
    return render(request, 'accounts/login.html')

# Registration Form
def register_page(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Check if the user already exists
        user_obj = User.objects.filter(username=email)
        
        if user_obj.exists():
            messages.success(request, "Email is already taken.")
            return HttpResponseRedirect(request.path_info)
        
        # Create a new user
        user_obj = User.objects.create(first_name=first_name, last_name=last_name, email=email, username=email)
        user_obj.set_password(password)
        user_obj.save()
        
        messages.success(request, "Sent on your mail verifications.")
        return HttpResponseRedirect(request.path_info)
        
    return render(request, 'accounts/register.html')


def activate_email(request , email_token):
    try:
        user = Profile.objects.get(email_token = email_token)
        user.is_email_verified = True
        user.save()
        return redirect('/')
    except Exception as e:
        return HttpResponse('Invalid Email token')
