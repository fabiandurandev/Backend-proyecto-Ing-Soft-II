from .models import Producto, Servicio
import django_filters

class ProductoFilter(django_filters.FilterSet):
    class Meta:
        model = Producto
        fields = {
            'nombreProducto': ['icontains']
        }

class ServicioFilter(django_filters.FilterSet):
    class Meta:
        model = Servicio
        fields = {
            'nombreServicio': ['icontains']
        }