from django import forms
from .models import Recipe, Review

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'quick_description', 'content', 'ingredients', 'picture']
        widgets = {
            'ingredients': forms.Textarea(attrs={'rows': 10}),
            'content': forms.Textarea(attrs={'rows': 8}),
            'quick_description': forms.Textarea(attrs={'rows': 4}),
        }


class ReviewForm(forms.ModelForm):
    RATING_CHOICES = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    ]
    rating = forms.ChoiceField(choices=RATING_CHOICES, widget=forms.Select)
    comment = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}))

    class Meta:
        model = Review
        fields = ('rating', 'comment')

