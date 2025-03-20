from django.shortcuts import get_object_or_404, render

from rest_framework.decorators import api_view,permission_classes
from .models import Product
from rest_framework.response import Response
from .serializers import ProductSerializers
from .filters import ProductsFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated


@api_view(['GET'])
def get_All_products(request):

    filterset = ProductsFilter(request.GET,queryset=Product.objects.all().order_by('id'))
    count = filterset.qs.count()
    resPage = 1
    paginator = PageNumberPagination()
    paginator.page_size = resPage

    queryset =  paginator.paginate_queryset(filterset.qs, request)
    serializer = ProductSerializers(queryset,many=True)
    return Response({"products":serializer.data, "per page":resPage, "count":count})

@api_view(['GET'])
def get_by_id_product(request, pk):
    product = get_object_or_404(Product, id=pk)
    serializer = ProductSerializers(product) 
    return Response({"product": serializer.data})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def new_product(request):
    serializer = ProductSerializers(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response({"product": serializer.data})
    
    return Response(serializer.errors, status=400)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_product(request, pk):
    product = get_object_or_404(Product, id=pk)

    if product.user != request.user:
        return Response({"error": "Sorry, you cannot update this product"}, status=403)
    
    serializer = ProductSerializers(product, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response({"product": serializer.data}, status=200)
    
    return Response(serializer.errors, status=400)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_product(request, pk):
    product = get_object_or_404(Product, id=pk)

    if product.user != request.user:
        return Response({"error": "Sorry, you cannot delete this product"}, status=403)

    product.delete()
    return Response({"details": "Product deleted successfully"}, status=204)

