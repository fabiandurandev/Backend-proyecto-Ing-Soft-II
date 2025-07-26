from django.shortcuts import get_object_or_404
from .models import (
    Producto,
    Venta,
    Cliente,
    Servicio,
    Proveedor,
    Empleado,
    Compra,
    TasaCambio,
    DetalleVentaProducto,
)
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
    RegistroUsuarioSerializer,
    TasaCambioSerializer,
    SolicitarCodigoSerializer,
    VerificarCodigoSerializer,
    CambiarContrasenaSerializer,
)
from rest_framework import generics, status
from .filters import ProductoFilter, ServicioFilter
from rest_framework.views import APIView
from django.utils.dateparse import parse_date
from datetime import datetime, time
from django.db import transaction
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer
from rest_framework.permissions import IsAuthenticated


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

    @transaction.atomic
    def patch(self, request, *args, **kwargs):
        venta = self.get_object()
        estado_nuevo = request.data.get("estadoVenta")

        if estado_nuevo == "ANUL" and venta.estadoVenta != "ANUL":
            # Recuperar productos de esa venta
            detalles = DetalleVentaProducto.objects.filter(venta=venta)

            for detalle in detalles:
                producto = detalle.producto
                producto.stock += detalle.cantidad
                producto.save()

        return self.partial_update(request, *args, **kwargs)


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


class CompraRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Compra.objects.all()
    serializer_class = CompraSerializer


class CompraPorFechaAPIView(APIView):
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

        compras = Compra.objects.filter(fecha__range=(fecha_inicio_dt, fecha_fin_dt))
        serializer = CompraSerializer(compras, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# api/views.py


class RegistroUsuarioAPIView(APIView):
    def post(self, request):
        serializer = RegistroUsuarioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Usuario creado correctamente"},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# api/views.py


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class TasaCambioAPIView(APIView):
    def get(self, request):
        ultima = TasaCambio.objects.order_by("-fecha").first()
        if ultima:
            serializer = TasaCambioSerializer(ultima)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            {"detail": "No hay tasa registrada"}, status=status.HTTP_404_NOT_FOUND
        )

    def post(self, request):
        serializer = TasaCambioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SolicitarCodigoView(APIView):
    def post(self, request):
        serializer = SolicitarCodigoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"mensaje": "Código enviado con éxito."}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerificarCodigoView(APIView):
    def post(self, request):
        serializer = VerificarCodigoSerializer(data=request.data)
        if serializer.is_valid():
            resultado = serializer.save()
            return Response(resultado, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CambiarContrasenaView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CambiarContrasenaSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"mensaje": "Contraseña cambiada exitosamente."},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
