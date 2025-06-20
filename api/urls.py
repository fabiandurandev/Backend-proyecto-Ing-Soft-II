from django.urls import path
from . import views

urlpatterns = [
    path('productos/', views.ProductoListaCreateAPIView.as_view()),
    path('ventas/', views.ventas_lista)
]
