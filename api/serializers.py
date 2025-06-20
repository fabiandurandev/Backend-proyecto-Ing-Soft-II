from rest_framework import serializers
from .models import Producto, Servicio, Venta, Empleado, Cliente, DetalleVentaServicio, DetalleVenta, DetalleVentaProducto

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = (
            'nombreCliente',
            'cedulaCliente'
        )

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = [
            'nombreProducto',
            'codigoProducto',
            'stock',
            'precioProducto',
        ]

class DetalleVentaProductoSerializer(serializers.ModelSerializer):
    nombreProducto = serializers.CharField(source='producto.nombreProducto')
    precioProducto = serializers.DecimalField(
        source='producto.precioProducto',
        max_digits=10,
        decimal_places=2
    )

    class Meta:
        model = DetalleVentaProducto
        fields = (
            'nombreProducto',
            'precioProducto',
            'cantidad',
            'producto_subtotal'
        )


class VentaSerializer(serializers.ModelSerializer):
    itemsProductos = DetalleVentaProductoSerializer(many=True, read_only=True)
    precio_total = serializers.SerializerMethodField()
    idCliente = ClienteSerializer()

    def get_precio_total(self,obj):
        ventaItems = obj.itemsProductos.all()
        return sum(ventaItem.producto_subtotal for ventaItem in ventaItems)

    class Meta:
        model = Venta
        fields = [
            'id',
            'idCliente',
            'idEmpleado',
            'estadoVenta',
            'itemsProductos',
            'precio_total'
        ]