from rest_framework import serializers
from .models import (
    Compra,
    Producto,
    Servicio,
    Venta,
    Empleado,
    Cliente,
    DetalleVentaServicio,
    DetalleVenta,
    DetalleVentaProducto,
    Proveedor,
    DetalleCompraProducto,
    TasaCambio,
)
from rest_framework.validators import UniqueValidator
from rest_framework import serializers
from .models import Usuario, Empleado
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.core.exceptions import ObjectDoesNotExist


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = (
            "id",
            "nombreCliente",
            "cedulaCliente",
            "direccionCliente",
            "telefonoCliente",
        )


class EmpleadoSerializer(serializers.ModelSerializer):

    cedulaEmpleado = serializers.IntegerField(
        validators=[
            UniqueValidator(
                queryset=Empleado.objects.all(), message="La cedula ya existe"
            )
        ]
    )

    class Meta:
        model = Empleado
        fields = "__all__"


class ProductoSerializer(serializers.ModelSerializer):
    codigoProducto = serializers.IntegerField(
        validators=[
            UniqueValidator(
                queryset=Producto.objects.all(), message="El codigo ya existe"
            )
        ]
    )

    class Meta:
        model = Producto
        fields = [
            "id",
            "nombreProducto",
            "codigoProducto",
            "stock",
            "precioProducto",
        ]


class ProveedorSerializer(serializers.ModelSerializer):
    rifProveedor = serializers.IntegerField(
        validators=[
            UniqueValidator(
                queryset=Proveedor.objects.all(), message="El rif ya existe"
            )
        ]
    )

    class Meta:
        model = Proveedor
        fields = "__all__"


class ServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servicio
        fields = [
            "id",
            "nombreServicio",
            "codigoServicio",
            "precioServicio",
        ]


class DetalleVentaProductoSerializer(serializers.ModelSerializer):
    # nombreProducto = serializers.CharField(source='producto.nombreProducto')
    # precioProducto = serializers.DecimalField(
    #     source='producto.precioProducto',
    #     max_digits=10,
    #     decimal_places=2
    # )

    class Meta:
        model = DetalleVentaProducto
        fields = (
            "producto",
            "nombreProducto",
            "precioProducto",
            "cantidad",
            "producto_subtotal",
        )


class DetalleVentaServicioSerializer(serializers.ModelSerializer):
    # nombreServicio = serializers.CharField(source='servicio.nombreServicio')
    # precioServicio = serializers.DecimalField(
    #     source='servicio.precioServicio',
    #     max_digits=10,
    #     decimal_places=2
    # )

    class Meta:
        model = DetalleVentaServicio
        fields = (
            "servicio",
            "nombreServicio",
            "precioServicio",
            "cantidad",
            "servicio_subtotal",
        )


class VentaCreateSerializer(serializers.ModelSerializer):

    class DetalleVentaProductoCreateSerializer(serializers.ModelSerializer):
        class Meta:
            model = DetalleVentaProducto
            fields = ("producto", "cantidad")

    class DetalleVentaServicioCreateSerializer(serializers.ModelSerializer):
        class Meta:
            model = DetalleVentaServicio
            fields = ("servicio", "cantidad")

    itemsProductos = DetalleVentaProductoCreateSerializer(many=True, required=False)
    itemsServicios = DetalleVentaServicioCreateSerializer(many=True, required=False)

    def create(self, validated_data):
        productos_data = validated_data.pop("itemsProductos", [])
        servicios_data = validated_data.pop("itemsServicios", [])
        try:
            ultima_tasa = TasaCambio.objects.latest("id")
            validated_data["tasaCambio"] = ultima_tasa.valor
        except ObjectDoesNotExist:
            raise serializers.ValidationError(
                "No hay ninguna tasa de cambio registrada."
            )

        venta = Venta.objects.create(**validated_data)

        for item in productos_data:
            producto = item["producto"]
            cantidad = item["cantidad"]
            DetalleVentaProducto.objects.create(
                venta=venta,
                producto=producto,
                cantidad=item["cantidad"],
                nombreProducto=producto.nombreProducto,
                precioProducto=producto.precioProducto,
            )

            producto.stock -= cantidad
            producto.save()

        # for item in servicios_data:
        #     DetalleVentaServicio.objects.create(venta=venta, servicio=item['servicio'], cantidad=item['cantidad'])

        for item in servicios_data:
            servicio = item["servicio"]
            DetalleVentaServicio.objects.create(
                venta=venta,
                servicio=servicio,
                cantidad=item["cantidad"],
                nombreServicio=servicio.nombreServicio,
                precioServicio=servicio.precioServicio,
            )

        return venta

    class Meta:
        model = Venta
        fields = [
            "idCliente",
            "idEmpleado",
            "estadoVenta",
            "itemsProductos",
            "itemsServicios",
        ]


class VentaSerializer(serializers.ModelSerializer):
    itemsProductos = DetalleVentaProductoSerializer(many=True, required=False)
    itemsServicio = DetalleVentaServicioSerializer(many=True, required=False)
    precio_total = serializers.SerializerMethodField()
    precio_total_bs = serializers.SerializerMethodField()
    idCliente = ClienteSerializer()
    idEmpleado = EmpleadoSerializer()

    def get_precio_total(self, obj):
        ventaItems = obj.itemsProductos.all()

        total_productos = sum(ventaItem.producto_subtotal for ventaItem in ventaItems)

        ventaItemsServicio = obj.itemsServicio.all()

        total_servicios = sum(
            ventaItem.servicio_subtotal for ventaItem in ventaItemsServicio
        )

        return total_productos + total_servicios

    def get_precio_total_bs(self, obj):
        total_usd = self.get_precio_total(obj)
        if obj.tasaCambio:
            return round(total_usd * obj.tasaCambio, 2)
        return None

    class Meta:
        model = Venta
        fields = [
            "id",
            "fecha",
            "idCliente",
            "idEmpleado",
            "estadoVenta",
            "itemsProductos",
            "itemsServicio",
            "tasaCambio",
            "precio_total",
            "precio_total_bs",
        ]


class DetalleCompraProductoSerializer(serializers.ModelSerializer):
    # nombreProducto = serializers.CharField(source='producto.nombreProducto')
    # precioProducto = serializers.DecimalField(
    #     source='producto.precioProducto',
    #     max_digits=10,
    #     decimal_places=2
    # )

    class Meta:
        model = DetalleCompraProducto
        fields = (
            "producto",
            "nombreProducto",
            "precioProducto",
            "cantidad",
            "producto_subtotal",
        )


class CompraSerializer(serializers.ModelSerializer):
    itemsProductosCompra = DetalleCompraProductoSerializer(many=True, required=False)
    precio_total_bs = serializers.SerializerMethodField()

    precio_total = serializers.SerializerMethodField()
    idProveedor = ProveedorSerializer()

    def get_precio_total(self, obj):
        compraItems = obj.itemsProductosCompra.all()

        total_productos = sum(
            compraItem.producto_subtotal for compraItem in compraItems
        )

        return total_productos

    def get_precio_total_bs(self, obj):
        total_usd = self.get_precio_total(obj)
        if obj.tasaCambio:
            return round(total_usd * obj.tasaCambio, 2)
        return None

    class Meta:
        model = Compra
        fields = [
            "id",
            "fecha",
            "idProveedor",
            "estadoCompra",
            "itemsProductosCompra",
            "precio_total",
            "precio_total_bs",
        ]


class CompraCreateSerializer(serializers.ModelSerializer):

    class DetalleCompraProductoCreateSerializer(serializers.ModelSerializer):
        class Meta:
            model = DetalleCompraProducto
            fields = ("producto", "cantidad")

    itemsProductosCompra = DetalleCompraProductoCreateSerializer(
        many=True, required=False
    )

    def create(self, validated_data):
        productos_data = validated_data.pop("itemsProductosCompra", [])

        try:
            ultima_tasa = TasaCambio.objects.latest("id")
            validated_data["tasaCambio"] = ultima_tasa.valor
        except ObjectDoesNotExist:
            raise serializers.ValidationError(
                "No hay ninguna tasa de cambio registrada."
            )

        compra = Compra.objects.create(**validated_data)

        for item in productos_data:
            producto = item["producto"]
            cantidad = item["cantidad"]
            DetalleCompraProducto.objects.create(
                compra=compra,
                producto=producto,
                cantidad=item["cantidad"],
                nombreProducto=producto.nombreProducto,
                precioProducto=producto.precioProducto,
            )

            producto.stock += cantidad
            producto.save()

        # for item in servicios_data:
        #     DetalleVentaServicio.objects.create(venta=venta, servicio=item['servicio'], cantidad=item['cantidad'])

        return compra

    class Meta:
        model = Compra
        fields = [
            "idProveedor",
            "estadoCompra",
            "itemsProductosCompra",
        ]


# api/serializers.py


class RegistroUsuarioSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=6)

    def validate_email(self, value):
        try:
            empleado = Empleado.objects.get(emailEmpleado=value)
        except Empleado.DoesNotExist:
            raise serializers.ValidationError("No existe un empleado con este correo.")

        if Usuario.objects.filter(email=value).exists():
            raise serializers.ValidationError("Ya existe un usuario con este correo.")

        if Usuario.objects.filter(empleado=empleado).exists():
            raise serializers.ValidationError(
                "Este empleado ya tiene un usuario registrado."
            )

        return value

    def create(self, validated_data):
        email = validated_data["email"]
        password = validated_data["password"]
        empleado = Empleado.objects.get(emailEmpleado=email)

        usuario = Usuario.objects.create(
            email=email,
            empleado=empleado,
            password=make_password(password),
            is_active=True,
            is_staff=(empleado.nivelAutorizacion == Empleado.NivelAutorizacion.admin),
        )
        return usuario


# api/serializers.py


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = "email"

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Puedes agregar info extra al token si quieres:
        token["email"] = user.email
        return token

    def validate(self, attrs):
        # Cambiar 'email' por 'username' internamente para que funcione
        attrs["username"] = attrs.get("email")
        return super().validate(attrs)


class TasaCambioSerializer(serializers.ModelSerializer):
    class Meta:
        model = TasaCambio
        fields = "__all__"
