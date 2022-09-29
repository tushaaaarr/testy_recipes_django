from django.contrib import admin

# Register your models here.

from .models import *

class RecipeImageAdmin(admin.StackedInline):
    model = RecipeImage

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = [RecipeImageAdmin]
    class Meta:
       model = Recipe

@admin.register(RecipeImage)
class RecipeImageAdmin(admin.ModelAdmin):
    pass