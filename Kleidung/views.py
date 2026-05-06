from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# JWT token views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.http import require_http_methods
from django.db.models import Q, Avg, Count
from django.core.paginator import Paginator
from django.contrib import messages
from .models import Listing, ListingImage, UserProfile, Favorite, Message, Review, Category
from .forms import (UserRegistrationForm, UserProfileForm, ListingForm, 
                    ListingImageForm, MessageForm, ReviewForm, SearchForm)


# ============== AUTHENTIFIZIERUNG ==============

def register(request):
    """Benutzerregistrierung"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Registrierung erfolgreich! Bitte melden Sie sich an.')
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'auth/register.html', {'form': form})


def login_view(request):
    """Benutzer-Login"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
        else:
            messages.error(request, 'Benutzername oder Passwort ungültig.')
    
    return render(request, 'auth/login.html')


def logout_view(request):
    """Benutzer-Logout"""
    logout(request)
    messages.success(request, 'Sie wurden erfolgreich abgemeldet.')
    return redirect('home')


# ============== STARTSEITE & SUCHE ==============

def home(request):
    """Startseite mit neuesten Angeboten"""
    listings = Listing.objects.filter(status='active').select_related('seller', 'category').prefetch_related('images')[:12]
    
    categories = Category.objects.all().annotate(
        active_count=Count('listing', filter=Q(listing__status='active'))
    )
    
    context = {
        'listings': listings,
        'categories': categories,
        'total_listings': Listing.objects.filter(status='active').count(),
    }
    return render(request, 'index.html', context)


def search_listings(request):
    """Suche und Filter für Angebote"""
    form = SearchForm(request.GET or None)
    listings = Listing.objects.filter(status='active').select_related('seller', 'category')
    
    # Filter anwenden
    query = request.GET.get('query', '')
    if query:
        listings = listings.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(brand__icontains=query) |
            Q(color__icontains=query)
        )
    
    min_price = request.GET.get('min_price')
    if min_price:
        listings = listings.filter(price__gte=min_price)
    
    max_price = request.GET.get('max_price')
    if max_price:
        listings = listings.filter(price__lte=max_price)
    
    condition = request.GET.get('condition')
    if condition:
        listings = listings.filter(condition=condition)
    
    location = request.GET.get('location')
    if location:
        listings = listings.filter(location__icontains=location)
    
    # Sortierung
    sort_by = request.GET.get('sort_by', '-created_at')
    listings = listings.order_by(sort_by)
    
    # Paginierung
    paginator = Paginator(listings, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'form': form,
        'page_obj': page_obj,
        'query': query,
    }
    return render(request, 'listings/search.html', context)


# ============== ANGEBOT DETAIL & VERWALTUNG ==============

def listing_detail(request, pk):
    """Detail-Seite für Angebot"""
    listing = get_object_or_404(Listing, pk=pk)
    
    # Views erhöhen
    listing.views += 1
    listing.save(update_fields=['views'])
    
    # Ähnliche Angebote
    similar_listings = Listing.objects.filter(
        status='active',
        category=listing.category
    ).exclude(pk=pk).select_related('seller')[:4]
    
    # Bewertung des Verkäufers
    seller_reviews = Review.objects.filter(seller=listing.seller)
    seller_rating = seller_reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    
    # Nachricht-Formular vorbereitet
    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(user=request.user, listing=listing).exists()
    
    context = {
        'listing': listing,
        'similar_listings': similar_listings,
        'seller_rating': seller_rating,
        'seller_review_count': seller_reviews.count(),
        'is_favorite': is_favorite,
    }
    return render(request, 'listings/detail.html', context)


@login_required(login_url='login')
def create_listing(request):
    """Neues Angebot erstellen"""
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.seller = request.user
            listing.save()
            
            # Bilder hochladen
            images = request.FILES.getlist('images')
            for i, image in enumerate(images):
                ListingImage.objects.create(
                    listing=listing,
                    image=image,
                    is_primary=(i == 0)  # Erstes Bild als Hauptbild
                )
            
            messages.success(request, 'Angebot erfolgreich erstellt!')
            return redirect('listing_detail', pk=listing.pk)
    else:
        form = ListingForm()
    
    context = {'form': form}
    return render(request, 'listings/create.html', context)


@login_required(login_url='login')
def edit_listing(request, pk):
    """Angebot bearbeiten"""
    listing = get_object_or_404(Listing, pk=pk)
    
    if listing.seller != request.user:
        return HttpResponseForbidden("Sie können dieses Angebot nicht bearbeiten.")
    
    if request.method == 'POST':
        form = ListingForm(request.POST, instance=listing)
        if form.is_valid():
            form.save()
            messages.success(request, 'Angebot aktualisiert!')
            return redirect('listing_detail', pk=listing.pk)
    else:
        form = ListingForm(instance=listing)
    
    context = {
        'form': form,
        'listing': listing,
    }
    return render(request, 'listings/edit.html', context)


@login_required(login_url='login')
def delete_listing(request, pk):
    """Angebot löschen"""
    listing = get_object_or_404(Listing, pk=pk)
    
    if listing.seller != request.user:
        return HttpResponseForbidden("Sie können dieses Angebot nicht löschen.")
    
    if request.method == 'POST':
        listing.delete()
        messages.success(request, 'Angebot gelöscht!')
        return redirect('my_listings')
    
    context = {'listing': listing}
    return render(request, 'listings/delete.html', context)


@login_required(login_url='login')
def my_listings(request):
    """Meine Angebote"""
    listings = request.user.listings.all().select_related('category').prefetch_related('images')
    
    # Filter nach Status
    status = request.GET.get('status')
    if status:
        listings = listings.filter(status=status)
    
    paginator = Paginator(listings, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'status': status,
    }
    return render(request, 'listings/my_listings.html', context)


# ============== FAVORITEN ==============

@login_required(login_url='login')
def toggle_favorite(request, pk):
    """Angebot zu Favoriten hinzufügen/entfernen"""
    listing = get_object_or_404(Listing, pk=pk)
    
    favorite, created = Favorite.objects.get_or_create(
        user=request.user,
        listing=listing
    )
    
    if not created:
        favorite.delete()
        return JsonResponse({'status': 'removed'})
    
    return JsonResponse({'status': 'added'})


@login_required(login_url='login')
def my_favorites(request):
    """Meine Favoriten"""
    favorites = Favorite.objects.filter(user=request.user).select_related('listing')
    
    paginator = Paginator(favorites, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {'page_obj': page_obj}
    return render(request, 'favorites.html', context)


# ============== NACHRICHTEN ==============

@login_required(login_url='login')
def messages_inbox(request):
    """Nachrichten-Posteingang"""
    messages_list = Message.objects.filter(recipient=request.user).order_by('-created_at')
    
    paginator = Paginator(messages_list, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {'message_list': page_obj}
    return render(request, 'messages/inbox.html', context)


@login_required(login_url='login')
def send_message(request, user_id):
    """Nachricht senden"""
    recipient = get_object_or_404(User, pk=user_id)
    listing_id = request.GET.get('listing')
    listing = None
    
    if listing_id:
        listing = get_object_or_404(Listing, pk=listing_id)
    
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.recipient = recipient
            message.listing = listing
            message.save()
            messages.success(request, 'Nachricht versendet!')
            return redirect('messages_inbox')
    else:
        initial = {}
        if listing:
            initial['subject'] = f"Re: {listing.title}"
        form = MessageForm(initial=initial)
    
    context = {
        'form': form,
        'recipient': recipient,
        'listing': listing,
    }
    return render(request, 'messages/send.html', context)


@login_required(login_url='login')
def message_detail(request, pk):
    """Einzelne Nachricht anzeigen"""
    message = get_object_or_404(Message, pk=pk)
    
    if message.recipient != request.user and message.sender != request.user:
        return HttpResponseForbidden("Sie können diese Nachricht nicht anzeigen.")
    
    # Nachricht als gelesen markieren
    if message.recipient == request.user and not message.is_read:
        message.is_read = True
        message.save()
    
    context = {'message': message}
    return render(request, 'messages/detail.html', context)


# ============== BENUTZER PROFILE ==============

def user_profile(request, username):
    """Benutzer-Profil anzeigen"""
    user = get_object_or_404(User, username=username)
    profile = user.profile
    
    # Aktive Angebote
    listings = user.listings.filter(status='active').select_related('category').prefetch_related('images')
    
    # Bewertungen
    reviews = Review.objects.filter(seller=user).select_related('reviewer')
    rating_avg = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    
    paginator = Paginator(listings, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'user': user,
        'profile': profile,
        'page_obj': page_obj,
        'reviews': reviews[:5],
        'rating_avg': rating_avg,
        'review_count': reviews.count(),
    }
    return render(request, 'users/profile.html', context)


@login_required(login_url='login')
def edit_profile(request):
    """Profil bearbeiten"""
    profile = request.user.profile
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profil aktualisiert!')
            return redirect('profile', username=request.user.username)
    else:
        form = UserProfileForm(instance=profile)
    
    context = {'form': form}
    return render(request, 'users/edit_profile.html', context)


@login_required(login_url='login')
def add_review(request, seller_id):
    """Bewertung hinzufügen"""
    seller = get_object_or_404(User, pk=seller_id)
    
    # Prüfe ob bereits bewertet
    existing_review = Review.objects.filter(reviewer=request.user, seller=seller).first()
    
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=existing_review)
        if form.is_valid():
            review = form.save(commit=False)
            review.reviewer = request.user
            review.seller = seller
            review.save()
            messages.success(request, 'Bewertung abgegeben!')
            return redirect('profile', username=seller.username)
    else:
        form = ReviewForm(instance=existing_review) if existing_review else ReviewForm()
    
    context = {
        'form': form,
        'seller': seller,
    }
    return render(request, 'reviews/add_review.html', context)


@login_required(login_url='login')
def create_listing(request):
    """Neues Angebot erstellen"""
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.seller = request.user
            listing.save()
            
            # Bilder verarbeiten
            images = request.FILES.getlist('images')
            for image in images:
                ListingImage.objects.create(listing=listing, image=image)
            
            messages.success(request, 'Angebot erfolgreich erstellt!')
            return redirect('listing_detail', pk=listing.pk)
    else:
        form = ListingForm()
    
    context = {'form': form}
    return render(request, 'listings/create.html', context)
