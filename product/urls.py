from django.urls import path
from .views import hello,create_product,get_products,get_product_detail, update_product,delete_product, get_product_by_category
from django.conf import settings
from django.conf.urls.static import static
urlpatterns=[
    path("hello/",hello),
    path('create/',create_product),
    path('get/',get_products),
    path('detail/<int:pk>/',get_product_detail),
    path('update/<int:pk>/',update_product),
    path('delete/<int:pk>/',delete_product),
    path("get_by_category/<str:category>/", get_product_by_category)
]


