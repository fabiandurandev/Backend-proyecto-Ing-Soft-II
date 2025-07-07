from django.shortcuts import get_object_or_404
from .models import Producto, Venta, Cliente, Servicio, Proveedor, Empleado, Compra
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import (
    ProductoSerializer,
    VentaSerializer,
    ClienteSerializer,
    VentaCreateSerializer,
    ServicioSerializer,
    ProveedorSerializer,
    EmpleadoSerializer,
    CompraCreateSerializer,
    CompraSerializer,
)
from rest_framework import generics
from .filters import ProductoFilter, ServicioFilter
from rest_framework.views import APIView
from rest_framework import status
from django.utils.dateparse import parse_date
from datetime import datetime, time


#   ---VISTA RELACIONADAS A PRODUCTOS---


class ProductoListaCreateAPIView(generics.ListCreateAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    filterset_class = ProductoFilter


class ProductoRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    lookup_field = "codigoProducto"

    # ---VISTAS RELACIONADAS A SERVICIOS---


class ServicioListCreateAPIView(generics.ListCreateAPIView):
    queryset = Servicio.objects.all()
    serializer_class = ServicioSerializer
    filterset_class = ServicioFilter


class ServicioRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Servicio.objects.all()
    serializer_class = ServicioSerializer
    lookup_field = "codigoServicio"

    # ---VISTAS RELACIONADAS A CLIENTES---


class ClienteListCreateAPIView(generics.ListCreateAPIView):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer


class ClienteRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    lookup_field = "cedulaCliente"

    # --VISTAS RELACIONADAS A EMPLEADOS--


class EmpleadoListCreateAPIView(generics.ListCreateAPIView):
    queryset = Empleado.objects.all()
    serializer_class = EmpleadoSerializer


class EmpleadoRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Empleado.objects.all()
    serializer_class = EmpleadoSerializer
    lookup_field = "cedulaEmpleado"


# --VISTAS RELACIONADAS A PROVEEDORES---


class ProveedorListCreateAPIView(generics.ListCreateAPIView):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer


class ProveedorRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer
    lookup_field = "rifProveedor"


# ---VISTA RELACIONADA A VENTAS---


class VentaListCreateAPIView(generics.ListCreateAPIView):
    queryset = Venta.objects.all()
    # serializer_class = VentaSerializer

    def get_serializer_class(self):
        if self.request.method == "POST":
            return VentaCreateSerializer
        return VentaSerializer


class VentaRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Venta.objects.all()
    serializer_class = VentaSerializer


class VentaPorFechaAPIView(APIView):
    def get(self, request):
        fecha_inicio = request.query_params.get("fechaInicio")
        fecha_fin = request.query_params.get("fechaFinal")

        if not fecha_inicio or not fecha_fin:
            return Response(
                {"error": "Debe proporcionar 'fechaInicio' y 'fechaFinal'."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        fecha_inicio_date = parse_date(fecha_inicio)
        fecha_fin_date = parse_date(fecha_fin)

        if not fecha_inicio_date or not fecha_fin_date:
            return Response(
                {"error": "Formato de fecha inválido. Debe ser YYYY-MM-DD."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Convertir a datetime con hora completa
        fecha_inicio_dt = datetime.combine(fecha_inicio_date, time.min)  # 00:00:00
        fecha_fin_dt = datetime.combine(fecha_fin_date, time.max)  # 23:59:59.999999

        ventas = Venta.objects.filter(fecha__range=(fecha_inicio_dt, fecha_fin_dt))
        serializer = VentaSerializer(ventas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CompraListCreateAPIView(generics.ListCreateAPIView):
    queryset = Compra.objects.all()
    # serializer_class = VentaSerializer

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CompraCreateSerializer
        return CompraSerializer
