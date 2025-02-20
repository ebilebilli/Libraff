from django.contrib import admin
from .models import Book

class BookAdmin(admin.ModelAdmin):
    # Fields to display in the list view
    list_display = ('title', 'author', 'price', 'like', 'pdf')  # Add 'pdf' here
    
    # Enable search functionality for title and author
    search_fields = ('title', 'author')
    
    # Add filters for price and author
    list_filter = ('price', 'author')
    
    # Fields to display in the detail/edit view
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'author')
        }),
        ('Pricing Information', {
            'fields': ('price', 'like')
        }),
        ('File Information', {
            'fields': ('pdf',)  # Add 'pdf' here for editing
        }),
    )
    
    # Ordering in the list view (e.g., by title)
    ordering = ('title',)
    
    # Optional: Add custom actions
    actions = ['set_price_to_zero']
    
    def set_price_to_zero(self, request, queryset):
        queryset.update(price=0)
    set_price_to_zero.short_description = "Set selected books' price to 0"

# Register the Book model with the customized admin class
admin.site.register(Book, BookAdmin)
