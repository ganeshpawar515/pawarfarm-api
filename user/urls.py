from rest_framework_simplejwt.views import TokenRefreshView
from django.urls import path
from .views import (hello_world,create_user,get_email_otp,verify_email_otp,CustomTokenObtainPairView,
                    user_profile,get_drivers_list,get_user_list,update_user,delete_user,get_live)




urlpatterns =[
    path('ping/',get_live,name="start-app"),
    path('token/',CustomTokenObtainPairView.as_view(),name='token_obtain_pair'),
    path('token/refresh/',TokenRefreshView.as_view(),name='token_refresh'),
    path('drivers/',get_drivers_list),
    path("user/hello/",hello_world),
    path("user/create/",create_user),
    path("user/profile/",user_profile),
    path("user/get_email_otp/",get_email_otp),
    path("user/verify_email_otp/",verify_email_otp),
    path("user/list/",get_user_list),
    path('api/user/<int:user_id>/update/', update_user, name='user-update'),
    path('api/user/<int:user_id>/delete/', delete_user, name='user-delete')
]