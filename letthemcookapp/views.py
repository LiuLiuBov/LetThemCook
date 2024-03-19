from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User, Recipe
from .forms import RecipeForm
from django.contrib.auth.decorators import login_required

def index_view(request):
    recipes = Recipe.objects.all()
    return render(request, "letthemcook/index.html", {'recipes': recipes})

def login_view(request):
    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "letthemcook/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "letthemcook/login.html")


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
            return render(request, "letthemcook/register.html", {
                "message": "Passwords must match."
            })

        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "letthemcook/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "letthemcook/register.html")

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
    return render(request, 'letthemcook/createrecipe.html', {'form': form})

@login_required
def saved(request):
    recipes = Recipe.objects.all()
    return render(request, 'letthemcook/saved.html', {'recipes': recipes})

@login_required
def profile(request):
    recipes = Recipe.objects.all()
    return render(request, 'letthemcook/profile.html', {'recipes': recipes})
    
def recipe(request, recipe_id):
    context_dict = {}
    try:
        recipe = Recipe.objects.get(id=recipe_id)
        context_dict['recipe'] = recipe
    except Recipe.DoesNotExist:
        context_dict['recipe'] = None
    
    return render(request, 'letthemcook/recipe.html', context=context_dict)
        