from django.contrib import admin
from .models import UserPreference

# Register your models here.
class AdminUserPreference(admin.ModelAdmin):
    pass

admin.site.register(UserPreference, AdminUserPreference)
