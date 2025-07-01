from django.contrib import admin
from .models import Venta, Cliente, Empleado, Producto, Servicio, DetalleVentaProducto, DetalleVentaServicio, DetalleVenta, Proveedor
# Register your models here.

admin.site.register(Venta)
admin.site.register(Cliente)
admin.site.register(Empleado)
admin.site.register(Servicio)
admin.site.register(Producto)
admin.site.register(DetalleVentaProducto)
admin.site.register(DetalleVentaServicio)
admin.site.register(DetalleVenta)
admin.site.register(Proveedor)