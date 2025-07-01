from django.shortcuts import get_object_or_404
from .models import Producto, Venta, Cliente, Servicio, Proveedor
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import ProductoSerializer, VentaSerializer, ClienteSerializer, VentaCreateSerializer, ServicioSerializer, ProveedorSerializer
from rest_framework import generics
from .filters import ProductoFilter, ServicioFilter



#   ---VISTA RELACIONADAS A PRODUCTOS---

class ProductoListaCreateAPIView(generics.ListCreateAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    filterset_class = ProductoFilter

class ProductoRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    lookup_field = 'codigoProducto'

    # ---VISTAS RELACIONADAS A SERVICIOS---

class ServicioListCreateAPIView(generics.ListCreateAPIView):
    queryset = Servicio.objects.all()
    serializer_class = ServicioSerializer
    filterset_class = ServicioFilter

   
    
class ServicioRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Servicio.objects.all()
    serializer_class = ServicioSerializer
    lookup_field = 'codigoServicio'

    # ---VISTAS RELACIONADAS A CLIENTES---

class ClienteListCreateAPIView(generics.ListCreateAPIView):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

class ClienteRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    lookup_field = 'cedulaCliente'

    # --VISTAS RELACIONADAS A PROVEEDORES---

class ProveedorListCreateAPIView(generics.ListCreateAPIView):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer

class ProveedorRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer
    lookup_field = 'riffProveedor'

# ---VISTA RELACIONADA A VENTAS---

class VentaListCreateAPIView(generics.ListCreateAPIView):
    queryset = Venta.objects.all()
    # serializer_class = VentaSerializer
    
    def get_serializer_class(self):
        if (self.request.method == 'POST'):
            return VentaCreateSerializer
        return VentaSerializer

