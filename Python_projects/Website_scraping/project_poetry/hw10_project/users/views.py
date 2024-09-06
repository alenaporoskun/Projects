from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

from .forms import RegisterForm, LoginForm, ProfileForm
from .models import Profile

def signupuser2(request):
    if request.user.is_authenticated:
        return redirect(to='quotes:root')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='quotes:login')
        else:
            return render(request, 'users/signup.html', context={"form": form})

    return render(request, 'users/signup.html', context={"form": RegisterForm()})


def loginuser(request):
    if request.user.is_authenticated:
        return redirect('main')

    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is None:
            messages.error(request, 'Username or password didn\'t match')
            return redirect(to='users:login')

        login(request, user)
        return redirect(to='quotes:root')

    return render(request, 'users/login.html', context={"form": LoginForm()})


@login_required
def logoutuser(request):
    logout(request)
    return redirect(to='quotes:root')


@login_required
def profile(request):
    # Отримати профіль користувача або створити новий, якщо він ще не існує
    profile_instance, created = Profile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile_instance)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='users:profile')

    profile_form = ProfileForm(instance=profile_instance)
    return render(request, 'users/profile.html', {'profile_form': profile_form})

def signupuser(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')  # Перенаправлення на сторінку входу
    else:
        form = UserCreationForm()
    return render(request, 'users/signup.html', {'form': form})