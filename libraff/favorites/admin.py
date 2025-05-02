from django.contrib import admin
from .models import Favorite

class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'book__title')
    ordering = ('-created_at',)
    
admin.site.register(Favorite, FavoriteAdmin)
