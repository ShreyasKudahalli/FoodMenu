from django.urls import path
from . import views
urlpatterns = [
    path('',views.login_user,name='login'),
    path('add-food/',views.add_food,name='add-food'),
    path('view-food/',views.view_food,name='view-food'),
    path('menu/<slug:slug>/', views.customer_menu, name='customer-menu'),
    path('my-qr/', views.my_qr, name='my-qr'),
    path('edit-food/<slug:slug>/', views.edit_food, name='edit-food'),
    path('delete-food/<slug:slug>/', views.delete_food, name='delete-food'),
    path('toggle-food/<slug:slug>/', views.toggle_food, name='toggle-food'),
]