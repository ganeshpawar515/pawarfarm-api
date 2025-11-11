from django.db import models
from django.conf import settings
from product.models import Product
from django.db.models import Q
from django.core.exceptions import ValidationError
# Create your models here.

class Order(models.Model):
    STATUS_CHOICES=(
        ('draft','In Cart'),
        ('pending','Pending'),
        ('assigned','Assigned'),
        ('on_way',"Left for Delivery"),
        ("delivered","Delivered"),
        ('cancelled',"Cancelled")
    )
    PAYMENT_CHOICES=(
        ("online","Online"),
        ("cash","Cash on delivery")
    )
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, related_name="orders")
    assigned_driver=models.ForeignKey(settings.AUTH_USER_MODEL,null=True,blank=True,on_delete=models.SET_NULL, related_name="delivery_orders")
    assigned_driver_name=models.CharField(max_length=100,blank=True,null=True)
    status=models.CharField(max_length=30,choices=STATUS_CHOICES,default='pending')
    created_at =models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=8,decimal_places=2,default=0)
    is_paid = models.BooleanField(default=False)
    payment_mode= models.CharField(max_length=30,choices=PAYMENT_CHOICES,blank=True,null=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    otp_code = models.CharField(max_length=6, null=True, blank=True)
    otp_created_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        constraints=[
            models.UniqueConstraint(
                fields=['user'],
                condition=Q(status='draft'),
                name='unique_draft_order_per_user'
            )
        ]

    def save(self, *args, **kwargs):
        if self.status=="draft" and self.is_paid:
            raise ValidationError("Cannot mark cart as paid")
        if self.assigned_driver:
            self.assigned_driver_name=self.assigned_driver.get_full_name() or self.assigned_driver.username or self.assigned_driver.email

        if self.pk:
            self.total_price = sum(
            item.price for item in self.items.all() if item.price is not None
        )
        if self.status == "delivered" and self.delivered_at is None:
             from django.utils import timezone
             self.delivered_at = timezone.now()
        super().save(*args,**kwargs)

    def update_total(self):
        self.total_price = sum(
            item.price for item in self.items.all() if item.price is not None
        )
        self.save(update_fields=["total_price"])
    def __str__(self):
        return f"Order {self.id} - {self.user.username}"
class OrderItem(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE,related_name='items')
    product=models.ForeignKey(Product,null=True,on_delete=models.SET_NULL)
    product_name = models.CharField(max_length=255,null=True,blank=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=8,decimal_places=2,blank=True,null=True)

    def save(self,*args,**kwargs):
        if self._state.adding and self.product and not self.product_name:
            self.product_name=self.product.name
        self.price=self.product.price*self.quantity
        super().save(*args,**kwargs)
        if self.order:
            self.order.save()