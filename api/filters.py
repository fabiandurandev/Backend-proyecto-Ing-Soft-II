from .models import Producto
import django_filters

class ProductoFilter(django_filters.FilterSet):
    class Meta:
        model = Producto
        fields = {
            'nombreProducto': ['icontains']
        }