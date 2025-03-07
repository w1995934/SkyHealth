from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = "skyhealth_home"),
    path('login/', views.login, name = "skyhealth_login"),
    path('review/', views.review, name = "skyhealth_review"),
    path('review/card/<int:id>/', views.card, name = "skyhealth_card")
]
