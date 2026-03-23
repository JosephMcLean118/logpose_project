
#kai-----------------------------------------------
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import UserProfile, Message 

# Create your views here.

def index(request):
    return render(request, 'logpose/base.html')


def profile_view(request, username):
    from django.contrib.auth.models import User
    target_user = get_object_or_404(User, username=username)

    profile, created = UserProfile.objects.get_or_create(user=target_user)
    
    messages = Message.objects.filter(receiver=target_user).order_by('-created_at')
    
    return render(request, 'profile.html', {
        'target_user': target_user,
        'profile': profile, 
        'messages': messages,
        'is_me': (request.user == target_user),
    })

def edit_profile(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        profile.bio = request.POST.get('bio', profile.bio)
        if 'profile_image' in request.FILES:
            profile.profile_image = request.FILES['profile_image']
        profile.save()
        return redirect('profile', username=request.user.username)
    
    return render(request, 'edit_profile.html', {'profile': profile})
#-------------------------------------------------------------------------