from rest_framework import viewsets
from .models import FoodItem
from .serializers import FoodItemSerializer

class FoodItemViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows viewing food items.
    """
    queryset = FoodItem.objects.all()
    serializer_class = FoodItemSerializer
