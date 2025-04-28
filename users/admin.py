from django.contrib import admin
from .models import CustomerUser 


class CustomerUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'bio', 'avatar', 'is_staff', 'date_joined')
    search_fields = ('username', 'email')
    list_filter = ('is_staff', 'is_active')
    ordering = ('-date_joined',)


# Register the models with the customized admin class
admin.site.register(CustomerUser, CustomerUserAdmin)


