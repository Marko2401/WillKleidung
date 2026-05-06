from django.urls import path, include
from . import views
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .api_views import (
    ListingViewSet, CategoryViewSet, UserViewSet,
    FavoriteViewSet, MessageViewSet, ReviewViewSet
)

router = routers.DefaultRouter()
router.register(r'listings', ListingViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'users', UserViewSet)
router.register(r'favorites', FavoriteViewSet)
router.register(r'messages', MessageViewSet)
router.register(r'reviews', ReviewViewSet)


urlpatterns = [
    # Authentifizierung
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Startseite und Suche
    path('', views.home, name='home'),
    path('search/', views.search_listings, name='search'),
    
    # Angebote
    path('listing/<int:pk>/', views.listing_detail, name='listing_detail'),
    path('listing/create/', views.create_listing, name='create_listing'),
    path('listing/<int:pk>/edit/', views.edit_listing, name='edit_listing'),
    path('listing/<int:pk>/delete/', views.delete_listing, name='delete_listing'),
    path('listing/<int:pk>/favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('my-listings/', views.my_listings, name='my_listings'),
    path('favorites/', views.my_favorites, name='my_favorites'),

    # Nachrichten
    path('messages/', views.messages_inbox, name='messages_inbox'),
    path('messages/send/<int:user_id>/', views.send_message, name='send_message'),
    path('messages/<int:pk>/', views.message_detail, name='message_detail'),

    # Profile
    path('profile/<str:username>/', views.user_profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    

    # API routes
    path('api/', include(router.urls)),
    path('api/auth/', include('rest_framework.urls')),  # browsable API login
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
