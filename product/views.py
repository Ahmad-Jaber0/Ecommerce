from django.shortcuts import render

from rest_framework.decorators import api_view
from .models import Product
from rest_framework.response import Response
from .serializers import ProductSerializers

@api_view(['GET'])
def get_All_products(request):
    product=Product.objects.all()
    serializers=ProductSerializers(product,many=True)

    return Response({"products":serializers.data})