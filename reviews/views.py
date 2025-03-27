from django.db.models import Avg
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Review
from product.models import Product  
from .serializers import ReviewSerializer

def update_product_rating(product):
    rating = product.reviews.aggregate(avg_ratings=Avg('rating'))['avg_ratings']
    product.rating = rating if rating is not None else 0
    product.save()

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_or_update_review(request, pk):
    user = request.user
    product = get_object_or_404(Product, id=pk)
    data = request.data

    rating = data.get('rating', 1)
    comment = data.get('comment', '').strip()

    if not (1 <= rating <= 5):
        return Response({"error": "Rating must be between 1 and 5"}, status=400)

    review, created = Review.objects.update_or_create(
        user=user,
        product=product,
        defaults={'rating': rating, 'comment': comment}
    )

    update_product_rating(product)
    return Response({'details': 'Rating created' if created else 'Rating updated'})


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_review(request, pk):
    user = request.user
    product = get_object_or_404(Product, id=pk)

    review = product.reviews.filter(user=user).first()
    if review:
        review.delete()
        update_product_rating(product)
        return Response({'details': 'Review deleted'})
    
    return Response({'error': 'Review not found'}, status=404)
