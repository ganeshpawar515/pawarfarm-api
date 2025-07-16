from django.contrib import admin
from .models import Order,OrderItem
# Register your models here.

class OrderAdmin(admin.ModelAdmin):
    list_display=['id','user','assigned_driver_name','total_price_calculated','status','is_paid']
    def total_price_calculated(self, obj):
        return sum(item.price for item in obj.items.all() if item.price)
    total_price_calculated.short_description="total price"
class OrderItemAdmin(admin.ModelAdmin):
    list_display=['id','order','product','price','quantity']
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderItem,OrderItemAdmin)
