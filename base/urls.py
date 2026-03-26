from django.urls import path
from . import views
urlpatterns = [
    path('',views.login_user,name='login'),
    path('add-food/',views.add_food,name='add-food'),
    path('view-food/',views.view_food,name='view-food'),
    path('menu/<slug:slug>/', views.customer_menu, name='customer-menu'),
    path('my-qr/', views.my_qr, name='my-qr'),
    path('create-admin/', views.create_admin),
]