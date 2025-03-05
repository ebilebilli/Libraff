from django.contrib import admin
from .models import Book, BookCategory


class BookCategoryAdmin(admin.ModelAdmin):
    """Admin configuration for managing BookCategory model."""
    list_display = ('category_name', 'book_count')  # Columns to display: category name and number of books
    search_fields = ('category_name',)  # Enable search by category name
    ordering = ('category_name',)  # Sort categories alphabetically

    def book_count(self, obj):
        """Calculate and display the number of books in this category."""
        return obj.book_set.count()
    book_count.short_description = "Book Count"  # Column header for book count


class BookAdmin(admin.ModelAdmin):
    """Admin configuration for managing Book model."""
    list_display = ('title', 'author', 'category', 'price', 'like', 'pdf', 'has_pdf')  # Columns to display in the list view
    search_fields = ('title', 'author', 'category__category_name')  # Search by title, author, and category name
    list_filter = ('price', 'author', 'category', 'like')  # Filters for price, author, category, and likes
    list_editable = ('price', 'like')  # Allow direct editing of price and likes from the list view
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'author', 'category', 'context')  # Group basic fields together
        }),
        ('Pricing & Popularity', {
            'fields': ('price', 'like')  # Group pricing and popularity fields
        }),
        ('File Information', {
            'fields': ('pdf',)  # Group file-related fields
        }),
    )
    ordering = ('-like', 'title')  # Sort by likes (descending) then title (ascending)
    actions = ['set_price_to_zero', 'increase_likes', 'clear_pdf']  # Custom actions for bulk operations
    list_per_page = 20  # Limit to 20 books per page in the list view

    # Custom column to indicate if a PDF is available
    def has_pdf(self, obj):
        """Check and display whether the book has a PDF file."""
        return bool(obj.pdf)
    has_pdf.boolean = True  # Display as a True/False icon
    has_pdf.short_description = "PDF Available?"  # Column header

    # Custom action to set price to zero
    def set_price_to_zero(self, request, queryset):
        """Set the price of selected books to 0."""
        updated = queryset.update(price=0)
        self.message_user(request, f"{updated} book(s) price set to 0.")  # Notify admin of the result
    set_price_to_zero.short_description = "Set selected books' price to 0"  # Action description

    # Custom action to increase likes
    def increase_likes(self, request, queryset):
        """Increase the likes of selected books by 10."""
        for book in queryset:
            book.like = (book.like or 0) + 10  # Handle null likes by defaulting to 0
            book.save()
        self.message_user(request, f"{queryset.count()} book(s) likes increased by 10.")  # Notify admin
    increase_likes.short_description = "Increase likes by 10"  # Action description

    # Custom action to clear PDF files
    def clear_pdf(self, request, queryset):
        """Remove PDF files from selected books."""
        updated = queryset.update(pdf=None)
        self.message_user(request, f"{updated} book(s) PDF cleared.")  # Notify admin
    clear_pdf.short_description = "Clear PDF from selected books"  # Action description


# Register models with their respective admin classes
admin.site.register(Book, BookAdmin)
admin.site.register(BookCategory, BookCategoryAdmin)