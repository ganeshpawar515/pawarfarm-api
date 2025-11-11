from django.db.models.signals import post_save
from django.dispatch import receiver
from order.models import Order
from payment.models import Payment
from decimal import Decimal

@receiver(post_save,sender=Order)
def create_delivery_payment(sender,instance,created,**kwargs):
    if not created and instance.status=='delivered':
        if not Payment.objects.filter(related_order=instance).exists():
            Payment.objects.create(
                user=instance.assigned_driver,
                payment_type='delivery_ride',
                related_order=instance,
                amount=(instance.total_price*Decimal('0.05')),
                status='pending'
            )
