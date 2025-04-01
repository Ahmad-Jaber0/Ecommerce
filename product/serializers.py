from rest_framework import serializers
from .models import Product
from reviews.serializers import ReviewSerializer

class ProductSerializer(serializers.ModelSerializer):
    reviews = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = "__all__"
        extra_kwargs = {
            'rating': {'read_only': True},
            'createdAt': {'read_only': True},
            'user': {'read_only': True},
            'id': {'read_only': True},
        }

    def get_reviews(self, obj):
        return ReviewSerializer(obj.reviews.all(), many=True).data
