from django.db import models

class FoodItem(models.Model):
    name = models.CharField(max_length=100, unique=True)
    calories = models.PositiveIntegerField()

    # Optional but recommended fields
    serving_size = models.CharField(max_length=50, blank=True, null=True)  # e.g. "100g", "1 cup"
    protein = models.FloatField(blank=True, null=True)   # grams
    fat = models.FloatField(blank=True, null=True)       # grams
    carbs = models.FloatField(blank=True, null=True)     # grams
    image_url = models.URLField(blank=True, null=True)   # to show image in Android app
    image = models.ImageField(upload_to="food_images/", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)

    def __str__(self):
        return f"{self.name} - {self.calories} kcal"
