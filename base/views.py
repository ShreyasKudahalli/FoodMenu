from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import Restaurant, FoodItem
from django.contrib.auth.decorators import login_required

from django.core.management import call_command
from django.http import HttpResponse

def migrate_db(request):
    call_command('migrate')
    return HttpResponse("Migration Done")

from django.contrib.auth.models import User

def create_admin(request):
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
        return HttpResponse("Admin created")
    return HttpResponse("Admin already exists")

def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Check if restaurant is active
            if hasattr(user, 'restaurant') and not user.restaurant.is_active:
                messages.error(request, "Your service is inactive. Please contact admin.")
                return redirect('login')

            login(request,user)
            return redirect('add-food')  # change to your page
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "Home/login.html")

@login_required
def add_food(request):
    if request.method == "POST":

        restaurant = request.user.restaurant   # 🔥 key line

        FoodItem.objects.create(
            restaurant=restaurant,   # 🔥 attach owner
            name=request.POST.get("name"),
            price=request.POST.get("price"),
            quantity=request.POST.get("quantity"),
            description=request.POST.get("description"),
            category=request.POST.get("category"),
            food_image=request.FILES.get("food_image")
        )

        messages.success(request, "Food item added successfully!")

        return redirect('add-food')

    return render(request,'Home/add-food.html')

@login_required
def view_food(request):

    restaurant = request.user.restaurant
    food_items = FoodItem.objects.filter(restaurant=restaurant)

    return render(request, 'Home/view-food.html', {'food_items': food_items})

def customer_menu(request, slug):
    restaurant = get_object_or_404(Restaurant, slug=slug)

    food_items = FoodItem.objects.filter(
        restaurant=restaurant
    )

    return render(request, 'Home/view-food.html', {
        'restaurant': restaurant,
        'food_items': food_items,
        'is_customer_view': True,
    })

@login_required
def my_qr(request):
    restaurant = request.user.restaurant

    return render(request, 'Home/my-qr.html', {
        'restaurant': restaurant
    })