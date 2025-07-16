from django.contrib import admin
from .models import Payment
# Register your models here.

class PaymentAdmin(admin.ModelAdmin):
    list_display=('user','payment_type','related_order','amount','status','paid_at')
admin.site.register(Payment,PaymentAdmin)
