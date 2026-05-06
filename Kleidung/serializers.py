from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Listing, ListingImage, Category, UserProfile, Favorite, Message, Review


class ListingImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListingImage
        fields = ['id', 'image', 'is_primary', 'uploaded_at']


class ListingSerializer(serializers.ModelSerializer):
    images = ListingImageSerializer(many=True, read_only=True)
    seller = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Listing
        fields = ['id', 'seller', 'title', 'description', 'category', 'size', 'price', 'color', 'brand', 'condition', 'status', 'location', 'created_at', 'updated_at', 'views', 'images']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'gender', 'icon']


class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = UserProfile
        fields = ['user', 'biography', 'profile_picture', 'location', 'phone', 'is_verified']


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'profile']


class FavoriteSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    listing = ListingSerializer(read_only=True)

    class Meta:
        model = Favorite
        fields = ['id', 'user', 'listing', 'created_at']


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.StringRelatedField(read_only=True)
    recipient = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'sender', 'recipient', 'listing', 'subject', 'text', 'created_at', 'is_read']


class ReviewSerializer(serializers.ModelSerializer):
    reviewer = serializers.StringRelatedField(read_only=True)
    seller = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'reviewer', 'seller', 'listing', 'rating', 'comment', 'created_at']
