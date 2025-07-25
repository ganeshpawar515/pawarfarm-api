from django.contrib import admin
from .models import Product
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display=['id',"name", "price", 'category','is_available', 'created_at']

admin.site.register(Product, ProductAdmin)