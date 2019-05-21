from django.contrib import admin

# Register your models here.
from .models import Product #import product class from models.py
#models.py and admin.py is in the same directory

admin.site.register(Product)