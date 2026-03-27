from django.db import models
from django.contrib.auth.models import User
import qrcode
from io import BytesIO
from django.core.files import File
from django.utils.text import slugify
import os

# Create your models here.\


class Restaurant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    restaurant_name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True, blank=True)
    
    is_active = models.BooleanField(default=True)
    subscription_end = models.DateField(null=True, blank=True)

    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)

    def __str__(self):
        return self.restaurant_name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.restaurant_name)

        super().save(*args, **kwargs)

        # ✅ Generate QR only if not exists
        if not self.qr_code:
            # Use the deployed domain or fallback to localhost for development
            base_url = os.environ.get('RENDER_EXTERNAL_HOSTNAME', '127.0.0.1:8000')
            protocol = 'https' if 'render.com' in base_url else 'http'
            url = f"{protocol}://{base_url}/menu/{self.slug}/"

            qr = qrcode.make(url)

            buffer = BytesIO()
            qr.save(buffer, format='PNG')

            file_name = f"{self.slug}_qr.png"
            self.qr_code.save(file_name, File(buffer), save=False)

            super().save(update_fields=['qr_code'])
    

class FoodItem(models.Model):

    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    CATEGORY_CHOICES = [
        ('veg', 'Vegetarian'),
        ('nonveg', 'Non-Vegetarian'),
        ('beverage', 'Beverage'),
        ('dessert', 'Dessert'),
    ]

    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField()
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    food_image = models.ImageField(upload_to='food_images/', null=True, blank=True)


    def __str__(self):
        return self.name