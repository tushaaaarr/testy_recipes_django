from django.db import models
from django.contrib.auth.models import User 
import jsonfield
from datetime import datetime


CATEGORY_CHOICES =(
    ("1", "Vegetarian"),
    ("2", "Non-Vegetarian"),
)
class Recipe(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    food_name = models.CharField(max_length=100)
    category = models.CharField(max_length=5,choices=CATEGORY_CHOICES)
    desc = models.TextField(default='' )
    ingredients = jsonfield.JSONField()
    steps =  jsonfield.JSONField()
    image = models.FileField(blank=True)
    pub_date=models.DateField(default=datetime.now())
    def __str__(self):
        return str(self.food_name)


class RecipeImage(models.Model):
    recipe = models.ForeignKey(Recipe, default=None, on_delete=models.CASCADE)
    images = models.FileField(upload_to = 'media')
    def __str__(self):
        return self.recipe.food_name