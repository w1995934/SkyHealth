from django.shortcuts import render, redirect

from .forms import UserForm, ProfileForm
from .models import Card, Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required



# Create your views here.
def home(request):
    return render(request, 'skyhealth/home.html')


def login(request):
    return render(request, 'skyhealth/login.html')


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('skyhealth_home')
    else:
        form = UserCreationForm()
    return render(request, 'skyhealth/signup.html', {'form': form})

@login_required
def review(request):
    cards = Card.objects.all()
    context = {'cards': cards}
    return render(request, 'skyhealth/review.html', context)

@login_required
def card(request, id):
    context = {'card': Card.objects.get(id=id)}
    return render(request, 'skyhealth/card.html', context)

@login_required
def profile_view(request, username):
    profile = Profile.objects.get(user__username=username)
    return render(request, 'skyhealth/profile.html', {'profile': profile})

def updateprofile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, f'Your profile was successfully updated!')
            return redirect('skyhealth_home')
        else:
            messages.error(request, f'Please correct the error below.')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'skyhealth/updateprofile.html', {
    'user_form': user_form,
    'profile_form': profile_form
    })
