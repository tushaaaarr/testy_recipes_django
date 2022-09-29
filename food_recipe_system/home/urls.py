
from django.urls import path,include
from . import views
urlpatterns = [
    path('',views.home,name='home'),
    path('login',views.login,name='login'),
    path('logout',views.logout,name='logout'),
    path('add_recipe',views.add_recipe,name='add_recipe'),
    path('view-recipe/<int:myid>',views.view_recipe,name='view_recipe'),
    path('update-recipe/<int:myid>',views.update_recipe,name='update_recipe'),
    path('recipe-search',views.search_recipe, name='search'),
    path('my-recipes',views.my_recipes,name='my_recipes'),

]
