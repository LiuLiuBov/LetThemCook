from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import redirect

from .models import Review, User, Recipe
from .forms import RecipeForm
from django.contrib.auth.decorators import login_required

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
    recipes = Recipe.objects.all()
    return render(request, 'createrecipe.html', {'recipes': recipes})

def saved(request):
    recipes = Recipe.objects.all()
    return render(request, 'saved.html', {'recipes': recipes})

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
        recipe_list = Recipe.objects.order_by('-title')

    return render(request,'index.html',{'recipes': recipe_list})
