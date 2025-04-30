from django import forms
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class CreateReviewForm(forms.Form):
    RATING_CHOICES = [
        (0, '0 - Not applicable'),
        (1, '1 - Needs improvement'),
        (2, '2 - Meets expectations'),
    ]

    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.RadioSelect)
