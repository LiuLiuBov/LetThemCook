from django import template
from letthemcookapp.models import Recipe

register = template.Library()

@register.inclusion_tag('recipe_list.html')
def get_recipe_list(current_recipe=None):
    return {'recipes': Recipe.objects.order_by('-average_rating'),
            'current_recipe': current_recipe}