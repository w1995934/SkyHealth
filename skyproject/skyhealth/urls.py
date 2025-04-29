from django.urls import path
from . import views
from django.contrib.auth import views as log_views

urlpatterns = [
    path('', views.home, name="skyhealth_home"),
    path('login/', log_views.LoginView.as_view(template_name='skyhealth/login.html'), name="skyhealth_login"),
    path('logout/', views.logout_user, name='skyhealth_logout'),
    path('signup/', views.signup, name="skyhealth_signup"),
    path('profile/<str:username>/', views.profile_view, name="skyhealth_profile_view"),
    path('updateprofile/', views.updateprofile, name="skyhealth_updateprofile"),
    path('cards/', views.cards, name="skyhealth_cards"),
    path('cards/<int:id>/', views.card, name="skyhealth_card"),
]