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

        return render(request,'Home/add-food.html')
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
        restaurant=restaurant
    )

    return render(request, 'Home/view-food.html', {
        'restaurant': restaurant,
        'food_items': food_items,
        'is_customer_view': True,
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