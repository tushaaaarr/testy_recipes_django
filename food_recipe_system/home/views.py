from unicodedata import category
from django.shortcuts import render,HttpResponse,redirect
from .models import *
import json
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as django_logout
from ast import literal_eval


def home(request):
    if request.GET.get('ordering'):
        ORD = request.GET.get('ordering')
        recipes = Recipe.objects.filter(category =ORD)
        return render(request,'user/index.html',{'recipes':recipes,'ordering':ORD})
    else:
        recipes = Recipe.objects.all()
        return render(request,'user/index.html',{'recipes':recipes})

@login_required(login_url='login')
def my_recipes(request):
    if request.GET.get('ordering'):
        ORD = request.GET.get('ordering')
        recipes = Recipe.objects.filter(category =ORD)
        return render(request,'user/index.html',{'recipes':recipes,'ordering':ORD})

    recipes = Recipe.objects.filter(user=request.user)
    return render(request,'user/my_recipes.html',{'recipes':recipes})    

def login(request):
    page_data = {}
    next = request.GET.get('next')
    if request.POST:
        loginusername = request.POST['username']
        loginpassword = request.POST['password']
        if User.objects.filter(username=loginusername).exists():
            user = authenticate(username=loginusername, password=loginpassword)
            if user is not None:
                auth.login(request, user)
                if next is not None:
                    return redirect(next)
                else:
                    return redirect('/')
            else:
                page_data['error'] = 'Invalid credentials! Please try again'

        else:
            page_data['error'] = "Account Not Found.."

    return render(request, 'auth/login.html', {'page_data': page_data})

def logout(request):
    django_logout(request)
    return redirect('/login')

@login_required(login_url='login')
def add_recipe(request):
    if request.POST:
        images=request.FILES.getlist("images")
        image=request.FILES.get("recipe_image")
        steps =  request.POST.getlist('steps')
        food_name = request.POST.get('name')
        desc = request.POST.get('desc')
        category = request.POST.get('category')
        ingrediants = request.POST.getlist('ingredients')
        step_list = list()
        for idx in range(len(images)):
            step_dict = {
            'step':steps[idx],
            'image':str(images[idx])
            }
            step_list.append(step_dict)
        new_recipe = Recipe(food_name = food_name, desc =desc ,image = image,category =category,
                            user = request.user,ingredients = ingrediants,steps = step_list)   
        new_recipe.save()
        for img in images:
            RecipeImage(recipe = new_recipe,images=img).save()

    return render(request,'user/add_recipe.html')

@login_required(login_url='login')
def view_recipe(request,myid):
    recipe = Recipe.objects.get(id = myid)
    return render(request,'user/view_recipe.html',{'recipe':recipe})

@login_required(login_url='login')
def update_recipe(request,myid):
    recipe = Recipe.objects.get(id = myid)
    if request.method == 'POST':
        image=request.FILES.get("recipe_image",None)
        images = request.FILES.getlist('images')
        steps =  request.POST.getlist('steps')
        food_name = request.POST.get('name')
        desc = request.POST.get('desc')
        category = request.POST.get('category')
        ingrediants = request.POST.getlist('ingredients')
        hidden_images = request.POST.getlist('hidden_imgs')
        step_list = []
  
        try:
            updated_imgs_with_id = literal_eval(json.loads(json.dumps(hidden_images))[0])
            id_list = [int(id_list['id']) - 1 for id_list in updated_imgs_with_id ]
        except:
            id_list = []

        for idx in range(len(steps)):
            if idx in id_list:
                img_path = [element['val'] for element in updated_imgs_with_id if int(element['id']) == idx + 1]
                for img in images:
                    if str(img) in img_path:   
                        RecipeImage(recipe = recipe,images=img).save()
                img_path = img_path[0]
            else:
                try:
                    img_path = str(recipe.steps[idx]['image'])
                except:
                    try:
                        img_path = str(images[idx])
                        for img in images:
                            if str(img) is img_path:   
                                RecipeImage(recipe = recipe,images=img).save()
                    except:
                        img_path = ' '
            step_dict = {
            'step':steps[idx],
            'image':img_path
            }
            step_list.append(step_dict)
                   
        if image is not None:
            ob = Recipe.objects.get(id=myid)
            ob.food_name = food_name
            ob.desc =desc
            ob.image = image
            ob.category =category
            ob.user = request.user
            ob.ingredients = ingrediants
            ob.steps = step_list
            ob.save()
        else:
            Recipe.objects.filter(id=myid).update(food_name = food_name, desc =desc, category =category,
                            user = request.user,ingredients = ingrediants,steps = step_list)

        return redirect(f'/view-recipe/{myid}')
    return render(request,'user/update_recipe.html',{'recipe':recipe})


@login_required(login_url='login')
def search_recipe(request):  
    if request.is_ajax(): 
        q = request.GET.get('term', '').capitalize()
        search_name = Recipe.objects.filter(food_name__contains=q)
        search_ingredient = Recipe.objects.filter(category__contains=q)
        search_qs = list(search_name) + list(search_ingredient)
        results = []
        for r in search_qs:
            if r.food_name not in results:
                results.append(r.food_name)
        data = json.dumps(results)
        return HttpResponse(data)
    elif request.GET.get('query'):
        q = request.GET.get('query', '').capitalize()
        search_name = Recipe.objects.filter(food_name__startswith=q)
        search_ingredient = Recipe.objects.filter(desc__icontains=q)
        search_qs = list(search_name) + list(search_ingredient)
        list_of_ids = [list_of_ids.id for list_of_ids in search_qs]
        filtered_recipes =  Recipe.objects.filter(pk__in=set(list(list_of_ids)))    
        return render(request,'user/index.html',{'recipes':filtered_recipes})
    
    