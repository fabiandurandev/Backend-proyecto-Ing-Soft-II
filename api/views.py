from django.shortcuts import get_object_or_404
from .models import Producto, Venta
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import ProductoSerializer, VentaSerializer
from rest_framework import generics
from .filters import ProductoFilter

# Create your views here.

@api_view(['GET'])
def producto_lista(request):
    productos = Producto.objects.all()
    serializer = ProductoSerializer(productos, many=True)
    filterset_class = ('nombreProducto',)

    return Response(serializer.data)

class ProductoListaCreateAPIView(generics.ListCreateAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    filterset_class = ProductoFilter


@api_view(['GET'])
def ventas_lista(request):
    ventas = Venta.objects.all()
    serializer = VentaSerializer(ventas, many=True)

    return Response(serializer.data)