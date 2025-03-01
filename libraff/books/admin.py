from django.contrib import admin
from .models import Book, BookCategory

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'price', 'like', 'pdf')
    search_fields = ('title', 'author')
    list_filter = ('price', 'author', 'category')
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'author', 'category')
        }),
        ('Pricing Information', {
            'fields': ('price', 'like')
        }),
        ('File Information', {
            'fields': ('pdf',)
        }),
    )
    ordering = ('title',)
    actions = ['set_price_to_zero']

    def set_price_to_zero(self, request, queryset):
        queryset.update(price=0)
    set_price_to_zero.short_description = "Set selected books' price to 0"

admin.site.register(Book, BookAdmin)
admin.site.register(BookCategory)
