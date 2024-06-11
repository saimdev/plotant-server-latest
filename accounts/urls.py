from django.urls import path, include
from . import views

urlpatterns = [
    path('signup', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('updateProfile', views.updateProfile),
    path('index', views.Authentication),
    path('updatePlan', views.stripe_payment),
    path('googleLogin', views.googleLogin),
    path('github/callback', views.github_callback),
    path('addCard', views.storeCard),
    path('getCards', views.getCard),
    path('deleteCard', views.deleteCard),
]