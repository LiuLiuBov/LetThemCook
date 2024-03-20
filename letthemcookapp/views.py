from django.shortcuts import redirect,render
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import numpy as np

from .models import Review, User, Recipe
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

def saved(request):
    recipes = Recipe.objects.all()
    return render(request, 'saved.html', {'recipes': recipes})

def profile(request):
    recipes = Recipe.objects.all()
    return render(request, 'profile.html', {'recipes': recipes})
    
def recipe(request, recipe_id):
    context_dict = {}
    
    try:
        recipe = Recipe.objects.get(id=recipe_id)
        context_dict['recipe'] = recipe
        context_dict['ingredients'] = recipe.ingredients.split('\n')
        context_dict['form'] = ReviewForm()
        
        reviews = Review.objects.filter(recipe=recipe_id)
        context_dict['reviews'] = reviews
        
        if(len(reviews) > 0):
            sum = np.sum(review.rating for review in reviews)
            mean = round(sum / len(reviews),2)
            context_dict['average'] = mean

    except Recipe.DoesNotExist:
        context_dict['recipe'] = None
        return redirect(reverse('letthemcook:index'))
    
    return render(request, 'recipe.html', context=context_dict)
        