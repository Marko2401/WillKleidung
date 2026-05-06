from rest_framework import viewsets, permissions
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Listing, Category, Favorite, Message, Review
from .serializers import (
    ListingSerializer, CategorySerializer, UserSerializer,
    FavoriteSerializer, MessageSerializer, ReviewSerializer
)


class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all().select_related('seller', 'category').prefetch_related('images')
    serializer_class = ListingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all().select_related('user', 'listing')
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # restrict to current user
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all().select_related('sender', 'recipient', 'listing')
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(Q(sender=user) | Q(recipient=user))

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all().select_related('reviewer', 'seller', 'listing')
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Optionally filter by seller id
        seller_id = self.request.query_params.get('seller')
        if seller_id:
            return self.queryset.filter(seller_id=seller_id)
        return self.queryset

    def perform_create(self, serializer):
        serializer.save(reviewer=self.request.user)
