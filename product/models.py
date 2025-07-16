from django.db import models

# Create your models here.

class Product(models.Model):
    CATEGORY_CHOICES=(
        ('milk', 'Milk'),
        ('eggs', 'Eggs'),
        ('fertilizer', 'Organic Fertilizer'),
        ('pickle', 'Pickle'),
        ('vegetable', 'Vegetable'),
        ('fruit', 'Fruit'),
        ('dairy', 'Milk Product'),
        ('other','Other')
    )
    name = models.CharField(max_length=150)
    description = models.TextField(null=True,blank=True)
    price =  models.DecimalField(max_digits=7,decimal_places=2)
    category = models.CharField(max_length=30,choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='product_images/')
    delivery_time = models.IntegerField(help_text="delivery time in days",default=7)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
