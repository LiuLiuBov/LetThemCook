from django.urls import path
from . import views

urlpatterns = [
    path("", views.index_view, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createrecipe", views.createrecipe, name="createrecipe"),
    path("saved", views.saved, name="saved"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("recipe/<int:recipe_id>/", views.recipe, name="recipe"),
    path("recipe/<int:recipe_id>/save/", views.save_recipe, name="save_recipe"),
    path("recipe/<int:recipe_id>/delete_recipe", views.delete_recipe,name="delete_recipe"),
    path("recipe/<int:recipe_id>/create_review/", views.create_review, name="create_review"),
    path("recipe/<int:recipe_id>/delete_save/", views.delete_save, name="deleterecipe"),
    path("suggest/", views.RecipeSuggestionView.as_view(), name='suggest'),
]
