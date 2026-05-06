from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime

class Category(models.Model):
    """Kleidungs-Kategorien"""
    GENDER_CHOICES = [
        ('M', 'Damen'),
        ('F', 'Herren'),
        ('K', 'Kinder'),
        ('U', 'Unisex'),
    ]
    
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    icon = models.CharField(max_length=50, default='shopping-bag')  # Für Frontend-Icons
    
    class Meta:
        verbose_name_plural = "Kategorien"
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.get_gender_display()})"


class Size(models.Model):
    """Größen für Kleidung"""
    SIZE_TYPE_CHOICES = [
        ('XS', 'Extra Small'),
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'X-Large'),
        ('XXL', '2X-Large'),
        ('XXXL', '3X-Large'),
        ('NUM', 'Numerisch (z.B. 36, 38)'),
    ]
    
    size = models.CharField(max_length=10)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='sizes')
    
    class Meta:
        unique_together = ('size', 'category')
        verbose_name_plural = "Größen"
    
    def __str__(self):
        return f"{self.category.name} - {self.size}"


class Listing(models.Model):
    """Kleidungs-Angebot/Listing"""
    STATUS_CHOICES = [
        ('active', 'Aktiv'),
        ('sold', 'Verkauft'),
        ('reserved', 'Reserviert'),
        ('inactive', 'Inaktiv'),
    ]
    
    CONDITION_CHOICES = [
        ('new', 'Neu'),
        ('like_new', 'Wie Neu'),
        ('very_good', 'Sehr Gut'),
        ('good', 'Gut'),
        ('acceptable', 'Befriedigend'),
    ]
    
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    size = models.ForeignKey(Size, on_delete=models.SET_NULL, null=True, blank=True)
    
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    color = models.CharField(max_length=50, blank=True)
    material = models.CharField(max_length=100, blank=True)
    brand = models.CharField(max_length=100, blank=True)
    
    condition = models.CharField(max_length=15, choices=CONDITION_CHOICES, default='very_good')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    
    location = models.CharField(max_length=200)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    views = models.IntegerField(default=0)
    
    class Meta:
        verbose_name_plural = "Listings"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['seller', '-created_at']),
            models.Index(fields=['category', 'status']),
            models.Index(fields=['status', '-created_at']),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.price}€ ({self.get_status_display()})"
    
    @property
    def main_image(self):
        return self.images.first()


class ListingImage(models.Model):
    """Bilder für Listings"""
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='listings/%Y/%m/%d/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_primary = models.BooleanField(default=False)
    
    class Meta:
        verbose_name_plural = "Listing Bilder"
        ordering = ['is_primary', 'uploaded_at']
    
    def __str__(self):
        return f"Bild für {self.listing.title}"


class Favorite(models.Model):
    """Favoriten der Benutzer"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'listing')
        verbose_name_plural = "Favoriten"
    
    def __str__(self):
        return f"{self.user.username} - {self.listing.title}"


class Message(models.Model):
    """Nachrichten zwischen Verkäufer und Käufer"""
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='messages', null=True, blank=True)
    
    subject = models.CharField(max_length=200, blank=True)
    text = models.TextField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    class Meta:
        verbose_name_plural = "Nachrichten"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient', '-created_at']),
            models.Index(fields=['sender', 'recipient']),
        ]
    
    def __str__(self):
        return f"{self.sender.username} → {self.recipient.username}: {self.subject or self.text[:50]}"


class Review(models.Model):
    """Bewertungen für Verkäufer"""
    RATING_CHOICES = [
        (1, '1 Stern'),
        (2, '2 Sterne'),
        (3, '3 Sterne'),
        (4, '4 Sterne'),
        (5, '5 Sterne'),
    ]
    
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_given')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_received')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='reviews', null=True, blank=True)
    
    rating = models.IntegerField(choices=RATING_CHOICES, validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Bewertungen"
        unique_together = ('reviewer', 'seller', 'listing')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.reviewer.username} bewertet {self.seller.username}: {self.rating}⭐"


class UserProfile(models.Model):
    """Erweiterte Benutzerprofile"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    biography = models.TextField(blank=True, max_length=500)
    profile_picture = models.ImageField(upload_to='profiles/%Y/%m/%d/', blank=True, null=True)
    location = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Benutzerprofile"
    
    def __str__(self):
        return f"Profil von {self.user.username}"
    
    @property
    def average_rating(self):
        reviews = self.user.reviews_received.all()
        if reviews.count() == 0:
            return 0
        return sum(r.rating for r in reviews) / reviews.count()
    
    @property
    def total_listings(self):
        return self.user.listings.count()
    
    @property
    def active_listings(self):
        return self.user.listings.filter(status='active').count()


# Signal to create user profile
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
