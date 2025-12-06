from rest_framework import serializers
from .models import FoodItem

class FoodItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodItem
        fields = [
            'id',
            'name',
            'calories',
            'serving_size',
            'protein',
            'fat',
            'carbs',
            'image',       # only if you added ImageField
            'image_url'    # only if you added URLField
        ]
