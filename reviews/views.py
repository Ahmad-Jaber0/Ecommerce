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

    rating = data.get('rating', 0)
    comment = data.get('comment', '').strip()

    if not (0 <= rating <= 5):
        return Response({"error": "يجب أن يكون التقييم بين 0 و 5"}, status=400)

    review, created = Review.objects.update_or_create(
        user=user,
        product=product,
        defaults={'rating': rating, 'comment': comment}
    )

    update_product_rating(product)
    return Response({'details': 'تم إنشاء التقييم' if created else 'تم تحديث التقييم'})


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_review(request, pk):
    user = request.user
    product = get_object_or_404(Product, id=pk)

    review = product.reviews.filter(user=user).first()
    if review:
        review.delete()
        update_product_rating(product)
        return Response({'details': 'تم حذف التقييم'})
    
    return Response({'error': 'لم يتم العثور على التقييم'}, status=404)
