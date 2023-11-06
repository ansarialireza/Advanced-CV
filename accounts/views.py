# accounts/views.py
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login, logout,authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.forms import PasswordResetForm
from django.core.mail import send_mail
from django.urls import reverse
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model

User = get_user_model()

def signup_view(request):
    if request.user.is_authenticated:
        messages.success(request, 'You are already logged in.')
        return redirect('/')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.email = request.POST['email']
            user = form.save(commit=False)
            user.is_active = False 
            user.save()
            # No login call here, so the user won't be logged in automatically
            messages.success(request, 'You have successfully registered.')
            return redirect('/')
    else:
        form = UserCreationForm()

    return render(request, 'registration/signup.html', {'form': form})



def login_view(request):
    if request.user.is_authenticated:
        messages.success(request, 'You are already logged in.')
        return redirect('/')  
    if request.method == 'POST': 
        username_or_email = request.POST['username_or_email']
        password = request.POST['password']
        user = authenticate(request, username=username_or_email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful. Welcome !')
            return redirect('/') 
        else:
            messages.error(request, 'Invalid login credentials. Please try again.')
    return render(request, 'registration/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'You have successfully logged out.')
    return redirect('/') 



def custom_password_reset(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
            except ObjectDoesNotExist:
                messages.error(request, 'Email not found. Please enter a valid email address.')
                return redirect('accounts:password_reset')

            # Generate a reset token and send the password reset email
            token = default_token_generator.make_token(user)
            uid = user.id
            reset_url = reverse('accounts:custom_password_reset_confirm', args=[uid, token])

            reset_url = request.build_absolute_uri(reset_url)

            subject = 'Password Reset'
            message = f'Use the following link to reset your password: {reset_url}'
            from_email = 'alireza@ansrza.ir'  # Replace with your email
            recipient_list = [email]
            send_mail(subject, message, from_email, recipient_list)

            return render(request, 'registration/custom_password_reset_done.html')
    else:
        form = PasswordResetForm()
    
    return render(request, 'registration/custom_password_reset.html', {'form': form})




def custom_password_reset_confirm(request, uidb64, token):
    if request.method == 'POST':
        user = get_object_or_404(User, pk=uidb64)
        if default_token_generator.check_token(user, token):
            new_password = request.POST.get('new_password')
            user.set_password(new_password)
            user.save()
            messages.success(request, 'Password reset successful. You can now log in with your new password.')
            return render(request, 'registration/custom_password_reset_complete.html')

    return PasswordResetConfirmView.as_view(
        template_name='registration/custom_password_reset_confirm.html',
        success_url='/custom_password_reset/complete/'
    )(request, uidb64=uidb64, token=token)

