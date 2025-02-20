from django.contrib import admin
from .models import CustomerUser, LikeBook, LikeComment


class CustomerUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'bio', 'avatar', 'is_staff', 'date_joined')
    search_fields = ('username', 'email')
    list_filter = ('is_staff', 'is_active')
    ordering = ('-date_joined',)


class LikeBookAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'created_at')
    search_fields = ('user__username', 'book__title')
    list_filter = ('created_at',)
    ordering = ('-created_at',)


class LikeCommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'comment', 'created_at')
    search_fields = ('user__username', 'comment__context')
    list_filter = ('created_at',)
    ordering = ('-created_at',)


# Register the models with the customized admin class
admin.site.register(CustomerUser, CustomerUserAdmin)
admin.site.register(LikeBook, LikeBookAdmin)
admin.site.register(LikeComment, LikeCommentAdmin)
