from django.shortcuts import render

# Card Data
cards = [
    {'id': 1, 'name': "Question 1"},
    {'id': 2, 'name': "Question 2"},
    {'id': 3, 'name': "Question 3"},
    {'id': 4, 'name': "Question 4"},
    {'id': 5, 'name': "Question 5"}
]

# Create your views here.
def home(request):
    return render(request, 'skyhealth/home.html')

def login(request):
    return render(request, 'skyhealth/login.html')

def review(request):
    context = {'cards':cards}
    return render(request, 'skyhealth/review.html', context)

def card(request, id):
    for card in cards:
        if card['id'] == id:
            context = {'card': card}
            break
    return render(request, 'skyhealth/card.html', context)
