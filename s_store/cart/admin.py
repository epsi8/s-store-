from django.contrib import admin
from .models import WishItem

@admin.register(WishItem)
class WishItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'created_at')
