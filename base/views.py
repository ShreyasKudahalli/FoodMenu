from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import Restaurant, FoodItem
from django.contrib.auth.decorators import login_required
import logging

logger = logging.getLogger(__name__)


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
    try:
        restaurant = request.user.restaurant
    except Restaurant.DoesNotExist as e:
        logger.error(f"Restaurant.DoesNotExist for user {request.user.username}: {str(e)}")
        messages.error(request, "You don't have a restaurant profile. Please contact admin.")
        return redirect('login')
    except Exception as e:
        logger.error(f"Unexpected error getting restaurant: {str(e)}", exc_info=True)
        messages.error(request, f"Error: {str(e)}")
        return redirect('login')
    
    try:
        if request.method == "POST":
            FoodItem.objects.create(
                restaurant=restaurant,
                name=request.POST.get("name"),
                price=request.POST.get("price"),
                quantity=request.POST.get("quantity"),
                description=request.POST.get("description"),
                category=request.POST.get("category"),
                food_image=request.FILES.get("food_image")
            )
            messages.success(request, "Food item added successfully!")
            return redirect('add-food')
        context = {
            'is_customer_view': False
        }

        return render(request,'Home/add-food.html', context)
    except Exception as e:
        logger.error(f"Error in add_food view for user {request.user.username}: {str(e)}", exc_info=True)
        raise  # Let Django handle it

@login_required
def view_food(request):
    try:
        restaurant = request.user.restaurant
    except Restaurant.DoesNotExist:
        messages.error(request, "You don't have a restaurant profile. Please contact admin.")
        return redirect('login')

    food_items = FoodItem.objects.filter(restaurant=restaurant)

    return render(request, 'Home/view-food.html', {'food_items': food_items})

def customer_menu(request, slug):
    restaurant = get_object_or_404(Restaurant, slug=slug)

    food_items = FoodItem.objects.filter(
        restaurant=restaurant,
        is_available=True
    )

    return render(request, 'Home/customer-menu.html', {
        'is_customer_view': True,
        'restaurant': restaurant,
        'food_items': food_items
    })

@login_required
def my_qr(request):
    try:
        restaurant = request.user.restaurant
    except Restaurant.DoesNotExist:
        messages.error(request, "You don't have a restaurant profile. Please contact admin.")
        return redirect('login')

    return render(request, 'Home/my-qr.html', {
        'restaurant': restaurant
    })

@login_required
def delete_food(request, slug):
    food = get_object_or_404(FoodItem, slug=slug, restaurant=request.user.restaurant)
    food.delete()
    messages.success(request, "Food deleted successfully!")
    return redirect('view-food')

@login_required
def toggle_food(request, slug):
    food = get_object_or_404(FoodItem, slug=slug, restaurant=request.user.restaurant)

    food.is_available = not food.is_available
    food.save()

    return redirect('view-food')

@login_required
def edit_food(request, slug):
    food = get_object_or_404(
        FoodItem,
        slug=slug,
        restaurant=request.user.restaurant
    )

    if request.method == "POST":
        food.name = request.POST.get("name")
        food.price = request.POST.get("price")
        food.quantity = request.POST.get("quantity")
        food.description = request.POST.get("description")
        food.category = request.POST.get("category")

        if request.FILES.get("food_image"):
            food.food_image = request.FILES.get("food_image")

        food.save()
        return redirect('view-food')

    return render(request, 'Home/edit-food.html', {'food': food})