from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.db.models import Avg
from django.shortcuts import render, redirect

from .forms import UserForm, CreateUserForm, CreateReviewForm
from .helper import *
from .models import Card, Profile, Review
from django.contrib import messages
from django.contrib.auth.decorators import login_required



# Home Page for app, accessible for all users
def home(request):
    return render(request, 'skyhealth/w1995934/home.html')

# Login Page, Uses Django's built-in functionality
# If User is already logged in, then they will be redirected to the homepage
class CustomLoginView(LoginView):
    template_name = 'skyhealth/w2011525/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('skyhealth_home')
        return super().dispatch(request, *args, **kwargs)

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
    return render(request, 'skyhealth/w2011525/register.html', {'form': form})

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
    split_description = split_card_description(card)
    context = {'card': card,
               'split_description': split_description}
    return render(request, 'skyhealth/card.html', context)

# View Users information, and is only able to view their own
# Requires User to be logged in
@login_required
def profile_view(request):
    profile = Profile.objects.get(user=request.user)
    return render(request, 'skyhealth/w2011525/profile.html', {'profile': profile, 'role': role_display_names(profile.role)})

# Allows the User to Update their information
# Requires User to be logged in
@login_required
def updateprofile(request):
    updateprofilehtml = 'skyhealth/w2011525/updateprofile.html'

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
            return render(request, updateprofilehtml, {'user_form': user_form})

        # Saves the form and updates the database with it
        if user_form.is_valid():
            user_form.save()
            messages.success(request, f'Your profile was successfully updated!')
            return redirect('skyhealth_home')
        else:
            messages.error(request, f'Please correct the error below.')
    else:
        # Returns the form with the users information
        user_form = UserForm(instance=request.user)
    return render(request, updateprofilehtml, {'user_form': user_form,})

# Logout user and redirects them to the Home screen with a message
# Requires User to be logged in
@login_required
def logout_user(request):
    logout(request)
    messages.success(request, "You Were Logged Out!")
    return redirect('skyhealth_home')


# The reviews that the Engineer and Team Leader can make
# Requires User to be logged in and be in a team
@login_required
def reviews(request):
    profile = request.user.profile

    if profile.role not in ['ENGINEER', 'TEAM_LEADER']:
        messages.warning(request, "Only Engineers and Team Leaders can create reviews.")
        return redirect('skyhealth_home')

    if not profile.teamID:
        messages.warning(request, "You currently are not in a Team.")
        return redirect('skyhealth_home')

    cards = Card.objects.all()

    user_reviews = Review.objects.filter(userID=profile)
    total_reviews = user_reviews.count()

    if total_reviews > 0:
        average_rating = round(user_reviews.aggregate(Avg('answer'))['answer__avg'], 1)

        # Convert from 0-2 scale to 1-3 scale
        average_rating = average_rating + 1
    else:
        average_rating = None

    return render(request, 'skyhealth/reviews.html', {'cards': cards, 'average_rating': average_rating})

@login_required
def create_review(request, card_id):
    # Get the User object
    profile = Profile.objects.get(user=request.user)

    # Checks if a valid User
    if profile.role not in ['ENGINEER', 'TEAM_LEADER']:
        messages.warning(request, "Only Engineers and Team Leaders can create reviews.")
        return redirect('skyhealth_home')

    # Checks if User has a team
    if not profile.teamID:
        messages.warning(request, "You are not in a team and cannot make reviews.")
        return redirect('skyhealth_home')

    # Gets the card and review data
    card = Card.objects.get(id=card_id)
    split_description = split_card_description(card)
    existing_review = Review.objects.filter(cardID=card, userID=profile).first()

    # Checks if it's a POST or GET request
    if request.method == 'POST':
        #
        form = CreateReviewForm(request.POST)

        if form.is_valid():
            rating = form.cleaned_data['rating']

            # Updates Review
            if existing_review:
                existing_review.answer = rating
                existing_review.save()
                messages.success(request, "Review updated!")
            # Creates Review from form
            else:
                Review.objects.create(
                    answer=rating,
                    cardID=card,
                    userID=profile)
                messages.success(request, "Review created!")

            return redirect('skyhealth_reviews')
        else:
            # Form validation failed
            messages.error(request, "Please select a valid rating.")
    else:
        # Provides a Empty form if no review is found
        # Sets the rating from the found review
        initial = {'rating': existing_review.answer} if existing_review else None
        form = CreateReviewForm(initial=initial)

    # Returns the card and its split description and review information and also the form
    return render(request, 'skyhealth/createreview.html', {
        'card': card,
        'split_description': split_description,
        'form': form,
        'existing_review': existing_review})
