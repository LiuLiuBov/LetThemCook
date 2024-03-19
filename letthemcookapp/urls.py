from django.urls import path

from . import views

urlpatterns = [
    path("", views.index_view, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("createrecipe/", views.createrecipe, name="createrecipe"),
    path("saved/", views.saved, name="saved"),
    path("profile/", views.profile, name="profile"),
]
