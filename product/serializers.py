from rest_framework import serializers
from .models import Product
from reviews.serializers import ReviewSerializer 

class ProductSerializers(serializers.ModelSerializer):
    reviews = serializers.SerializerMethodField(method_name='get_reviews', read_only=True)

    class Meta:
        model = Product
        fields = "__all__"

    def get_reviews(self, obj):
        reviews = obj.reviews.all()
        return ReviewSerializer(reviews, many=True).data
