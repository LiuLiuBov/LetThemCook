from django.shortcuts import get_object_or_404, redirect,render
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views import View
import numpy as np
from django.contrib import messages

from .models import Review, Save, User, Recipe
from .forms import RecipeForm,ReviewForm

def index_view(request):
    recipes = Recipe.objects.all()
    return render(request, "index.html", {'recipes': recipes})

def login_view(request):
    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "login.html")

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def recipe(request, recipe_id):
    context_dict = {}

    try:
        recipe_obj = Recipe.objects.get(id=recipe_id)
        recipe_obj.update_average()
        recipe_obj.update_saves()
        context_dict['recipe'] = recipe_obj
        context_dict['content'] = recipe_obj.content.split('\n')
        context_dict['ingredients'] = recipe_obj.ingredients.split('\n')
        context_dict['form'] = ReviewForm()
        context_dict['creator'] = recipe_obj.user

        reviews = Review.objects.filter(recipe=recipe_id)
        context_dict['reviews'] = reviews

        if request.user.is_authenticated:
            is_saved = Save.objects.filter(user=request.user, recipe=recipe_obj).exists()
        else:
            is_saved = False
        context_dict['is_saved'] = is_saved

        if reviews:
            context_dict['average'] = round(recipe_obj.average_rating, 2)
        else:
            context_dict['average'] = "No reviews yet"

    except Recipe.DoesNotExist:
        context_dict['recipe'] = None
        return HttpResponseRedirect(reverse('index'))

    return render(request, 'recipe.html', context=context_dict)

@login_required
def delete_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id, user=request.user)
    recipe.delete()
    messages.success(request, "Recipe deleted successfully.")
    return redirect('index')


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "register.html", {
                "message": "Passwords must match."
            })

        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "register.html")

@login_required
def createrecipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.user = request.user
            recipe.save()
            return redirect('index')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = RecipeForm()
    return render(request, 'createrecipe.html', {'form': form})


@login_required
def create_review(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    
    # Check if the recipe belongs to the logged-in user
    if recipe.user == request.user:
        messages.error(request, "You cannot review your own recipe.")
        return redirect('recipe', recipe_id=recipe_id)
    
    existing_review = Review.objects.filter(recipe=recipe, user=request.user).exists()
    
    if existing_review:
        messages.error(request, "You have already reviewed this recipe.")
        return redirect('recipe', recipe_id=recipe_id)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.recipe = recipe
            review.user = request.user
            review.save()
            recipe.update_average()
            messages.success(request, "Your review has been added.")
            return redirect('recipe', recipe_id=recipe_id)
        else:
            messages.error(request, "There was an error with your submission.")
    else:
        form = ReviewForm()
    
    return redirect('recipe', recipe_id=recipe_id)

@login_required
def delete_review(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)
        

@login_required
def save_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    saved_instance, created = Save.objects.get_or_create(user=request.user, recipe=recipe)
    recipe.update_saves()
    if not created:
        saved_instance.delete()
    return redirect('recipe', recipe_id=recipe_id)


def delete_save(request, recipe_id):
    recipe= get_object_or_404(Recipe, id=recipe_id)
    saved_instance = Save.objects.get(user=request.user, recipe=recipe)
    saved_instance.delete()
    
    return redirect('profile', request.user.username)

def saved(request):
    user = request.user
    saved_recipes = Recipe.objects.filter(save__user=user).distinct()
    return render(request, 'saved.html', {'saved_recipes': saved_recipes})

@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)
    user_recipes = Recipe.objects.filter(user=user)
    user_reviews = Review.objects.filter(user=user).order_by('-created_at')
    saved_recipes = Recipe.objects.filter(save__user=user).distinct()
    
    return render(request, 'profile.html', {'username': user.username,
        'user_recipes': user_recipes,
        'user_reviews': user_reviews,
        'saved_recipes' : saved_recipes
    })

class RecipeSuggestionView(View):
    def get(self, request):
        if 'suggestion' in request.GET:
            suggestion = request.GET['suggestion']
        else:
            suggestion = ''

        recipe_list = get_recipe_list(max_results=8,
                starts_with=suggestion)
        
        if len(recipe_list) == 0:
            recipe_list = Recipe.objects.order_by('-average_rating')

        return render(request,'recipe_list.html',{'recipes': recipe_list})

def get_recipe_list(max_results=0, starts_with=''):
    recipe_list = []

    if starts_with:
        recipe_list = Recipe.objects.filter(title__istartswith=starts_with)

    if max_results > 0:
        if len(recipe_list) > max_results:
            recipe_list = recipe_list[:max_results]

    return recipe_list