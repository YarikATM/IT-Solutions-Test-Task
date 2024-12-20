from django.urls import path
from . import views

urlpatterns = [
    path('login', views.user_login, name="users.login"),
    path('logout', views.user_logout, name="users.logout"),
    path('register', views.user_registration, name="users.register"),
    path('profile', views.user_profile, name="users.profile"),
]
