from django.contrib.auth import logout
from django.shortcuts import render, redirect

from .forms import UserForm, CreateUserForm
from .models import Card, Profile
from django.contrib import messages
from django.contrib.auth.decorators import login_required



# Home Page for app, accessible for all users
def home(request):
    return render(request, 'skyhealth/home.html')

# Login Page, Uses Django's built-in functionality
def login(request):
    return render(request, 'skyhealth/login.html')

# User Register Page
def signup(request):
    if request.method == 'POST':
        # Validate form and create the new user with a default role of ENGINEER
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()

            profile = user.profile  # This works because of the signal we have in models.py
            profile.role = 'ENGINEER'
            profile.save()

            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('skyhealth_login')
    else:
        # Returns an empty form to create user
        form = CreateUserForm()
    return render(request, 'skyhealth/signup.html', {'form': form})

# Displays all cards that a User can create a review for
# Requires User to be logged in
@login_required
def cards(request):
    cards = Card.objects.all()
    context = {'cards': cards}
    return render(request, 'skyhealth/cards.html', context)

# Displays the specific card
# Requires User to be logged in
@login_required
def card(request, id):
    card = Card.objects.get(id=id)
    split_description = [part.strip() for part in card.cardDetail.split('Or.') if part.strip()]
    context = {'card': card,
               'split_description': split_description}
    return render(request, 'skyhealth/card.html', context)

# View Users information, and is only able to view their own
# Requires User to be logged in
@login_required
def profile_view(request, username):
    profile = Profile.objects.get(user__username=username)

    if  request.user.username != username:
        return redirect('skyhealth_home')
    return render(request, 'skyhealth/profile.html', {'profile': profile})

# Allows the User to Update their information
# Requires User to be logged in
@login_required
def updateprofile(request):
    if request.method == 'POST':
        # Validate POST request is valid
        user_form = UserForm(request.POST, instance=request.user)

        # Get the submitted data
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()

        # Validate that fields are not empty
        if not first_name or not last_name or not email:
            messages.error(request, "Fields cannot be empty.")
            return render(request, 'skyhealth/updateprofile.html', {'user_form': user_form})

        if user_form.is_valid():
            user_form.save()
            messages.success(request, f'Your profile was successfully updated!')
            return redirect('skyhealth_home')
        else:
            messages.error(request, f'Please correct the error below.')
    else:
        # Returns the form with the users information
        user_form = UserForm(instance=request.user)
    return render(request, 'skyhealth/updateprofile.html', {'user_form': user_form,})

# Logout user and redirects them to the Home screen with a message
# Requires User to be logged in
@login_required
def logout_user(request):
    logout(request)
    messages.success(request, "You Were Logged Out!")
    return redirect('skyhealth_home')