from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Size, Listing, ListingImage, Favorite, Message, Review, UserProfile

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'gender', 'get_size_count']
    list_filter = ['gender']
    search_fields = ['name', 'description']
    
    def get_size_count(self, obj):
        return obj.sizes.count()
    get_size_count.short_description = 'Anzahl der Größen'


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ['size', 'category']
    list_filter = ['category']
    search_fields = ['size']


class ListingImageInline(admin.TabularInline):
    model = ListingImage
    extra = 1
    fields = ['image', 'is_primary', 'uploaded_at']
    readonly_fields = ['uploaded_at']


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ['title', 'seller', 'price', 'status', 'category', 'condition', 'created_at', 'thumbnail']
    list_filter = ['status', 'condition', 'category', 'created_at']
    search_fields = ['title', 'seller__username', 'description']
    readonly_fields = ['views', 'created_at', 'updated_at']
    inlines = [ListingImageInline]
    
    fieldsets = (
        ('Grundinformationen', {
            'fields': ('seller', 'title', 'description', 'category')
        }),
        ('Details', {
            'fields': ('size', 'price', 'condition', 'brand', 'color', 'material', 'location')
        }),
        ('Status', {
            'fields': ('status', 'views')
        }),
        ('Zeitstempel', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def thumbnail(self, obj):
        if obj.main_image:
            return format_html(
                '<img src="{}" width="50" height="50" style="object-fit: cover;" />',
                obj.main_image.image.url
            )
        return "Keine Bilder"
    thumbnail.short_description = 'Vorschau'


@admin.register(ListingImage)
class ListingImageAdmin(admin.ModelAdmin):
    list_display = ['listing', 'image_preview', 'is_primary', 'uploaded_at']
    list_filter = ['is_primary', 'uploaded_at']
    readonly_fields = ['image_preview', 'uploaded_at']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="100" height="100" style="object-fit: cover;" />',
                obj.image.url
            )
        return "Keine Bild"
    image_preview.short_description = 'Vorschau'


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['user', 'listing', 'created_at']
    list_filter = ['created_at', 'user']
    search_fields = ['user__username', 'listing__title']
    readonly_fields = ['created_at']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'recipient', 'subject_preview', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at', 'sender']
    search_fields = ['sender__username', 'recipient__username', 'subject', 'text']
    readonly_fields = ['created_at']
    
    def subject_preview(self, obj):
        return obj.subject or obj.text[:50]
    subject_preview.short_description = 'Betreff'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['reviewer', 'seller', 'rating_stars', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['reviewer__username', 'seller__username', 'comment']
    readonly_fields = ['created_at', 'updated_at']
    
    def rating_stars(self, obj):
        stars = '⭐' * obj.rating
        return format_html(stars)
    rating_stars.short_description = 'Bewertung'


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'location', 'is_verified', 'rating_display', 'total_listings', 'created_at']
    list_filter = ['is_verified', 'created_at']
    search_fields = ['user__username', 'user__email', 'location']
    readonly_fields = ['created_at', 'updated_at', 'profile_picture_preview']
    
    def profile_picture_preview(self, obj):
        if obj.profile_picture:
            return format_html(
                '<img src="{}" width="150" height="150" style="object-fit: cover; border-radius: 50%;" />',
                obj.profile_picture.url
            )
        return "Keine Profilbild"
    profile_picture_preview.short_description = 'Profilbild'
    
    def rating_display(self, obj):
        avg = obj.average_rating
        if avg > 0:
            stars = '⭐' * int(avg)
            return format_html(f'{stars} ({avg:.1f})')
        return "Noch keine Bewertungen"
    rating_display.short_description = 'Bewertung'
