from django.contrib import admin
from .models import User
# import pytz
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display=['id',"username",'email','role','is_staff','is_superuser','is_email_verified','date_joined','indian_time']
    readonly_fields=["indian_time"]
    def indian_time(self,obj):
        # tz=pytz.timezone("Asia/Kolkata")
        return obj.date_joined.astimezone().strftime("%B %d, %Y, %H:%M")

    indian_time.short_description="Date Joined (IST)"

admin.site.register(User, UserAdmin)