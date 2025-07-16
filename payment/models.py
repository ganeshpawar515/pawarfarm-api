from pawarfarm import settings
from django.db import models
from order.models import Order
# Create your models here.

class Payment(models.Model):
    PAYMENT_TYPE_CHOICES=(
    ('delivery_ride', 'Delivery Ride'),
    ('salary', 'Salary'),
    ('bonus', 'Bonus'),
    ('adjustment', 'Adjustment'),
    )
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
        ]
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    payment_type=models.CharField(max_length=20,choices=PAYMENT_TYPE_CHOICES)
    related_order=models.ForeignKey(Order,on_delete=models.CASCADE,null=True,blank=True)
    amount=models.DecimalField(max_digits=8,decimal_places=2,default=0)
    status=models.CharField(max_length=20,choices=STATUS_CHOICES,default='pending')
    paid_at=models.DateTimeField(null=True,blank=True)
    remarks=models.TextField(null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)