from django.shortcuts import get_object_or_404, render

from rest_framework.decorators import api_view,permission_classes
from .models import Product
from rest_framework.response import Response
from .serializers import ProductSerializers
from .filters import ProductsFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

def paginate_queryset(queryset, request, page_size=10):
    """Helper function to apply pagination."""
    paginator = PageNumberPagination()
    paginator.page_size = page_size
    result_page = paginator.paginate_queryset(queryset, request)
    return result_page, paginator


@api_view(['GET'])
def get_all_products(request):

    filtered_products = ProductsFilter(request.GET, queryset=Product.objects.all().order_by('id')).qs
    count = filtered_products.count()
    
    queryset, paginator = paginate_queryset(filtered_products, request, page_size=10)
    serializer = ProductSerializers(queryset, many=True)
    return Response({"products":serializer.data, "count":count})

@api_view(['GET'])
def get_by_id_product(request, pk):
    product = get_object_or_404(Product, id=pk)
    serializer = ProductSerializers(product) 
    return Response({"product": serializer.data},status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def new_product(request):
    serializer = ProductSerializers(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response({"product": serializer.data},status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_product(request, pk):
    product = get_object_or_404(Product, id=pk)

    if product.user != request.user:
        return Response({"error": "Sorry, you cannot update this product"}, status=status.HTTP_403_FORBIDDEN)
    
    serializer = ProductSerializers(product, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response({"product": serializer.data}, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=400)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_product(request, pk):
    product = get_object_or_404(Product, id=pk)

    if product.user != request.user:
        return Response({"error": "Sorry, you cannot delete this product"}, status=status.HTTP_403_FORBIDDEN)

    product.delete()
    return Response({"details": "Product deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

