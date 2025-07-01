from django.urls import path
from . import views

urlpatterns = [
    path('productos/', views.ProductoListaCreateAPIView.as_view()),
    path('producto/<int:codigoProducto>', views.ProductoRetrieveUpdateDestroyAPIView.as_view()),
    path('servicios/', views.ServicioListCreateAPIView.as_view()),
    path('servicio/<int:codigoServicio>', views.ServicioRetrieveUpdateDestroyAPIView.as_view()),
    path('clientes/', views.ClienteListCreateAPIView.as_view()),
    path('clientes/<int:cedulaCliente>', views.ClienteRetrieveUpdateDestroyAPIView.as_view()),
    path('proveedores/', views.ProveedorListCreateAPIView.as_view()),
    path('proveedor/<int:riffProveedor>', views.ProveedorRetrieveUpdateDestroyAPIView.as_view()),
    
    path('ventas/', views.VentaListCreateAPIView.as_view())
]
