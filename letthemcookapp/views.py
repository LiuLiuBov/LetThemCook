from django.shortcuts import get_object_or_404, redirect,render
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import numpy as np

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


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def recipe(request, recipe_id):
    context_dict = {}

    try:
        recipe_obj = Recipe.objects.get(id=recipe_id)
        context_dict['recipe'] = recipe_obj
        context_dict['ingredients'] = recipe_obj.ingredients.split('\n')
        context_dict['form'] = ReviewForm()

        reviews = Review.objects.filter(recipe=recipe_id)
        context_dict['reviews'] = reviews

        if request.user.is_authenticated:
            is_saved = Save.objects.filter(user=request.user, recipe=recipe_obj).exists()
        else:
            is_saved = False
        context_dict['is_saved'] = is_saved

        if reviews:
            avg_rating = np.mean([review.rating for review in reviews])
            context_dict['average'] = round(avg_rating, 2)
        else:
            context_dict['average'] = "No reviews yet"

    except Recipe.DoesNotExist:
        context_dict['recipe'] = None
        return redirect(reverse('index'))

    return render(request, 'recipe.html', context=context_dict)


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
        form = RecipeForm()
    return render(request, 'createrecipe.html', {'form': form})

@login_required
def create_review(request, recipe_id):
    print(recipe_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            review = Review(recipe=Recipe.objects.get(id=recipe_id), user=request.user, rating=form.cleaned_data["rating"])
            review.comment = form.cleaned_data["comment"]
            review.save()
            return redirect('index')
    else:
        form = ReviewForm()
    
    return redirect('index')

@login_required
def save_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    saved_instance, created = Save.objects.get_or_create(user=request.user, recipe=recipe)
    if not created:
        saved_instance.delete()
    return redirect('recipe', recipe_id=recipe_id)


@login_required
def saved(request):
    user = request.user
    saved_recipes = Recipe.objects.filter(save__user=user).distinct()
    return render(request, 'saved.html', {'saved_recipes': saved_recipes})


@login_required
def profile(request):
    recipes = Recipe.objects.all()
    return render(request, 'profile.html', {'recipes': recipes})

def get_recipe_list(max_results=0, starts_with=''):
    recipe_list = []

    if starts_with:
        recipe_list = Recipe.objects.filter(title__istartswith=starts_with)

    if max_results > 0:
        if len(recipe_list) > max_results:
            recipe_list = recipe_list[:max_results]

    return recipe_list

def get_recipes(request):
    if 'suggestion' in request.GET:
        suggestion = request.GET['suggestion']
    else:
        suggestion = ''

    category_list = get_recipe_list(max_results=8, starts_with=suggestion)

    if len(category_list) == 0:
        recipe_list = Recipe.objects.order_by('title')

    return render(request,'index.html',{'recipes': recipe_list})