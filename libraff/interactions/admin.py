from django.contrib import admin
from .models import Comment, Like


class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'comment', 'created_at')
    search_fields = ('user__username', 'book__title', 'comment__content')
    list_filter = ('created_at', 'user')


admin.site.register(Like, LikeAdmin)