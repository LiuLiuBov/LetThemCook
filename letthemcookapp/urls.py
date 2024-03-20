from django.urls import path

from . import views

urlpatterns = [
    path("", views.index_view, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createrecipe", views.createrecipe, name="createrecipe"),
    path("saved", views.saved, name="saved"),
    path("profile", views.profile, name="profile"),
    path("recipe/<int:recipe_id>/", views.recipe, name="recipe"),
    #No recipe view so code crashes
    path("recipe/<int:recipe_id>/create_review/", views.create_review, name="create_review"),
]
