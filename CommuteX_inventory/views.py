from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import SignUpForm


def landing(request):
    return render(request, 'landing.html')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('landing')  # ✅ no namespace

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('landing')  # ✅ no namespace
        else:
            messages.error(request, 'Login failed. Please check your username/password.')
    else:
        form = AuthenticationForm(request)

    form.fields['username'].widget.attrs.update({'placeholder': 'Your username'})
    form.fields['password'].widget.attrs.update({'placeholder': 'Your password'})

    return render(request, 'login.html', {'form': form})


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('landing')  # ✅ no namespace

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('landing')  # ✅ no namespace
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = SignUpForm()

    return render(request, 'signup.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'You are logged out.')
    return redirect('landing')  # ✅ no namespace
