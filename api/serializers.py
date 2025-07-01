from rest_framework import serializers
from .models import Producto, Servicio, Venta, Empleado, Cliente, DetalleVentaServicio, DetalleVenta, DetalleVentaProducto, Proveedor

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = (
            'id',
            'nombreCliente',
            'cedulaCliente',
            'direccionCliente',
            'telefonoCliente'
        )

class EmpleadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empleado
        fields = '__all__'

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = [
            'id',
            'nombreProducto',
            'codigoProducto',
            'stock',
            'precioProducto',
        ]

class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = '__all__'

class ServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servicio
        fields = [
            'id',
            'nombreServicio',
            'codigoServicio',
            'precioServicio',
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
            'nombreServicio',
            'precioServicio',
            'cantidad',
            'servicio_subtotal'
        )

class VentaCreateSerializer(serializers.ModelSerializer):

    class DetalleVentaProductoCreateSerializer(serializers.ModelSerializer):
        class Meta:
            model = DetalleVentaProducto
            fields = ('producto', 'cantidad')

    class DetalleVentaServicioCreateSerializer(serializers.ModelSerializer):
        class Meta:
            model = DetalleVentaServicio
            fields = ('servicio', 'cantidad')

    itemsProductos = DetalleVentaProductoCreateSerializer(many=True, required=False)
    itemsServicios = DetalleVentaServicioCreateSerializer(many=True, required=False)

    def create(self, validated_data):
            productos_data = validated_data.pop('itemsProductos', [])
            servicios_data = validated_data.pop('itemsServicios', [])

            venta = Venta.objects.create(**validated_data)

            for item in productos_data:
                DetalleVentaProducto.objects.create(venta=venta, producto=item['producto'], cantidad=item['cantidad'])
            
            # for item in servicios_data:
            #     DetalleVentaServicio.objects.create(venta=venta, servicio=item['servicio'], cantidad=item['cantidad'])

            for item in servicios_data:
                servicio = item['servicio']
                DetalleVentaServicio.objects.create(
                    venta=venta,
                    servicio=servicio,
                    cantidad=item['cantidad'],
                    nombreServicio=servicio.nombreServicio,
                    precioServicio=servicio.precioServicio
            )

            return venta

    class Meta:
        model = Venta
        fields = [
            'idCliente',
            'idEmpleado',
            'estadoVenta',
            'itemsProductos',
            'itemsServicios',   
        ]

class VentaSerializer(serializers.ModelSerializer):
    itemsProductos = DetalleVentaProductoSerializer(many=True, required=False)
    itemsServicio = DetalleVentaServicioSerializer(many=True, required=False)
    precio_total = serializers.SerializerMethodField()
    idCliente = ClienteSerializer()
    idEmpleado = EmpleadoSerializer()

    def get_precio_total(self,obj):
        ventaItems = obj.itemsProductos.all()

        total_productos =  sum(ventaItem.producto_subtotal for ventaItem in ventaItems)

        ventaItemsServicio = obj.itemsServicio.all()

        total_servicios =  sum(ventaItem.servicio_subtotal for ventaItem in ventaItemsServicio)

        return total_productos + total_servicios

    class Meta:
        model = Venta
        fields = [
            'id',
            'fecha',
            'idCliente',
            'idEmpleado',
            'estadoVenta',
            'itemsProductos',
            'itemsServicio',
            'precio_total'
        ]