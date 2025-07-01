from django.shortcuts import get_object_or_404
from .models import Producto, Venta, Cliente, Servicio
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import ProductoSerializer, VentaSerializer, ClienteSerializer, VentaCreateSerializer, ServicioSerializer
from rest_framework import generics
from .filters import ProductoFilter, ServicioFilter

# Create your views here.

# @api_view(['GET'])
# def producto_lista(request):
#     productos = Producto.objects.all()
#     serializer = ProductoSerializer(productos, many=True)
#     filterset_class = ('nombreProducto',)

#     return Response(serializer.data)

class ProductoListaCreateAPIView(generics.ListCreateAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    filterset_class = ProductoFilter

class ProductoRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    lookup_field = 'codigoProducto'

class ServicioListCreateAPIView(generics.ListCreateAPIView):
    queryset = Servicio.objects.all()
    serializer_class = ServicioSerializer
    filterset_class = ServicioFilter

    def create(self, request, *args, **kwargs):
        print("DATA RECIBIDA:", request.data)
        return super().create(request, *args, **kwargs)

class ClienteListCreateAPIView(generics.ListAPIView):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

class ClienteRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    lookup_field = 'cedulaCliente'

class ServicioRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Servicio.objects.all()
    serializer_class = ServicioSerializer
    lookup_field = 'codigoServicio'

class VentaListCreateAPIView(generics.ListCreateAPIView):
    queryset = Venta.objects.all()
    # serializer_class = VentaSerializer
    
    def get_serializer_class(self):
        if (self.request.method == 'POST'):
            return VentaCreateSerializer
        return VentaSerializer

# @api_view(['GET'])
# def ventas_lista(request):
#     ventas = Venta.objects.all()
#     serializer = VentaSerializer(ventas, many=True)

#     return Response(serializer.data)