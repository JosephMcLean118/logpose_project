from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from logpose.forms import UserForm, UserProfileForm


def index(request):
    return render(request, 'logpose/base.html')


def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_image' in request.FILES:
                profile.profile_image = request.FILES['profile_image']

            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'logpose/register.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'registered': registered,
    })


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('logpose:index'))
            else:
                return render(request, 'logpose/login.html', {
                    'error': 'Your account has been disabled.',
                })
        else:
            return render(request, 'logpose/login.html', {
                'error': 'Invalid username or password.',
            })
    else:
        return render(request, 'logpose/login.html')


@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('logpose:index'))
