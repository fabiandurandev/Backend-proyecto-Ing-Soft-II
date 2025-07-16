from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("productos/", views.ProductoListaCreateAPIView.as_view()),
    path(
        "producto/<int:codigoProducto>",
        views.ProductoRetrieveUpdateDestroyAPIView.as_view(),
    ),
    path("servicios/", views.ServicioListCreateAPIView.as_view()),
    path(
        "servicio/<int:codigoServicio>",
        views.ServicioRetrieveUpdateDestroyAPIView.as_view(),
    ),
    path("clientes/", views.ClienteListCreateAPIView.as_view()),
    path("empleados/", views.EmpleadoListCreateAPIView.as_view()),
    path(
        "empleado/<int:cedulaEmpleado>",
        views.EmpleadoRetrieveUpdateDestroyAPIView.as_view(),
    ),
    path(
        "cliente/<int:cedulaCliente>",
        views.ClienteRetrieveUpdateDestroyAPIView.as_view(),
    ),
    path("proveedores/", views.ProveedorListCreateAPIView.as_view()),
    path(
        "proveedor/<int:rifProveedor>",
        views.ProveedorRetrieveUpdateDestroyAPIView.as_view(),
    ),
    path("ventas/", views.VentaListCreateAPIView.as_view()),
    path("venta/<int:pk>", views.VentaRetrieveUpdateDestroyAPIView.as_view()),
    path(
        "ventas/por-fechas/",
        views.VentaPorFechaAPIView.as_view(),
        name="ventas_por_fechas",
    ),
    path("compras/", views.CompraListCreateAPIView.as_view()),
    path("compra/<int:pk>", views.CompraRetrieveUpdateDestroyAPIView.as_view()),
    path(
        "compras/por-fechas/",
        views.CompraPorFechaAPIView.as_view(),
        name="compras_por_fechas",
    ),
    path("registro_usuario/", views.RegistroUsuarioAPIView.as_view()),
    path(
        "api/token/",
        views.CustomTokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
