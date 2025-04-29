from django.contrib.auth import logout
from django.shortcuts import render, redirect

from .forms import UserForm, CreateUserForm
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
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('skyhealth_login')
    else:
        form = CreateUserForm()
    return render(request, 'skyhealth/signup.html', {'form': form})

@login_required
def review(request):
    cards = Card.objects.all()
    context = {'cards': cards}
    return render(request, 'skyhealth/review.html', context)

@login_required
def card(request, id):
    card = Card.objects.get(id=id)
    split_description = [part.strip() for part in card.cardDetail.split('Or.') if part.strip()]
    context = {'card': card,
               'split_description': split_description}
    return render(request, 'skyhealth/card.html', context)

@login_required
def profile_view(request, username):
    profile = Profile.objects.get(user__username=username)
    return render(request, 'skyhealth/profile.html', {'profile': profile})

@login_required
def updateprofile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, f'Your profile was successfully updated!')
            return redirect('skyhealth_home')
        else:
            messages.error(request, f'Please correct the error below.')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'skyhealth/updateprofile.html', {'user_form': user_form,})

@login_required
def logout_user(request):
    logout(request)
    messages.success(request, "You Were Logged Out!")
    return redirect('skyhealth_home')