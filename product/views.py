from django.shortcuts import get_object_or_404, render

from rest_framework.decorators import api_view
from .models import Product
from rest_framework.response import Response
from .serializers import ProductSerializers
from .filters import ProductsFilter
from rest_framework.pagination import PageNumberPagination


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