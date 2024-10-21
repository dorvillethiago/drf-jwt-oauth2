from django.contrib import admin
from .models import CustomUser


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "is_staff", "provider")

    def __str__(self):
        return "User"
