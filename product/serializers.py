from rest_framework import serializers
from .models import Product
from reviews.serializers import ReviewSerializer

class ProductSerializer(serializers.ModelSerializer):
    reviews = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = "__all__"
        read_only_fields = ['rating','createdAt','user']

    def get_reviews(self, obj):
        return ReviewSerializer(obj.reviews.all(), many=True).data
