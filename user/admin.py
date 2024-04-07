from django.contrib import admin

from user.models import User


@admin.register(User)
class AdminTest(admin.ModelAdmin):
    list_display = ['email']