from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Cliente(models.Model):
    class EstadoCliente(models.TextChoices):
        activo = 'ACT', 'Activo'
        desactivo = 'DES', 'Desactivo'

    cedulaCliente = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(999999999)], 
        unique=True,
        )
    nombreCliente = models.CharField(max_length=100)
    direccionCliente = models.CharField(max_length=255)
    telefonoCliente = models.CharField(max_length=100)
    estado = models.CharField(max_length=3, choices=EstadoCliente.choices, default=EstadoCliente.activo)

    def __str__(self):
        return self.nombreCliente

class Empleado(models.Model):
    class NivelAutorizacion(models.TextChoices):
        admin = 'ADMIN', 'Administrador'
        empleado = 'EMP', 'Empleado'

    nombreEmpleado = models.CharField(max_length=100)
    cedulaEmpleado = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(999999999)],
        unique=True
    )
    direccionEmpleado = models.CharField(max_length=150)
    telefonoEmpleado = models.CharField(max_length=100)
    emailEmpleado = models.EmailField(max_length=250)
    nivelAutorizacion = models.CharField(
        max_length=5, 
        choices=NivelAutorizacion.choices, 
        default=NivelAutorizacion.empleado
        )
    
    def __str__(self):
        return self.nombreEmpleado
    
class Producto(models.Model):
    nombreProducto = models.CharField(max_length=100)
    codigoProducto = models.PositiveIntegerField(
        validators=[MinValueValidator(1), 
                    MaxValueValidator(999999999)], 
                    unique=True
                    )
    stock = models.PositiveIntegerField()
    precioProducto = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nombreProducto

class Servicio(models.Model):
    codigoServicio = models.PositiveBigIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(999999999)],
        unique=True
    )
    precioServicio = models.DecimalField(max_digits=10, decimal_places=2)
    nombreServicio = models.CharField(max_length=100)

    def __str__(self):
        return self.nombreServicio

class Venta(models.Model):
    class EstadoVenta(models.TextChoices):
        valido = 'VAL', 'Valido'
        anulado = 'ANUL', 'Anulado'

    fecha = models.DateTimeField(auto_now_add=True)
    idCliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True)
    idEmpleado = models.ForeignKey(Empleado, on_delete=models.SET_NULL, null=True)
    estadoVenta = models.CharField(
        max_length=4, 
        choices=EstadoVenta.choices, 
        default=EstadoVenta.valido
        )
    productos = models.ManyToManyField(Producto, through='DetalleVentaProducto', related_name='ventasProductos')
    servicios = models.ManyToManyField(Servicio, through='DetalleVentaServicio', related_name='ventasServicios')

    def __str__(self):
        return f"Venta {self.id}"

class DetalleVentaProducto(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='itemsProductos')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()

    @property
    def producto_subtotal(self):
        return self.producto.precioProducto * self.cantidad
    
    def __str__(self):
        return f"{self.cantidad} x {self.producto} en Venta {self.venta.id}"
    
class DetalleVentaServicio(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='itemsServicio')
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    nombreServicio = models.CharField(max_length=100,null=True, blank=True)
    precioServicio = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    @property
    def servicio_subtotal(self):
        return self.precioServicio * self.cantidad
    
    def __str__(self):
        return f"{self.cantidad} x {self.servicio} en Venta {self.venta.id}"
    
class DetalleVenta(models.Model):
    ventaDetalle = models.OneToOneField(Venta, on_delete=models.CASCADE)
    nombreCliente = models.CharField(max_length=100) 
    cedulaCliente = models.PositiveIntegerField()

    def __str__(self):
        return f"Detalle de vetan: {self.ventaDetalle} - Cliente: {self.nombreCliente}"
    

class Proveedor(models.Model):
    riffProveedor = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(999999999)],
        unique=True)
    nombreProveedor = models.CharField(max_length=100)
    email = models.EmailField(max_length=250)
    telefonoProveedor = models.CharField(max_length=100)
    direccionProveedor = models.CharField(max_length=250)
    fechaRegistro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Proveedor: {self.nombreProveedor} - Riff: {self.riffProveedor}"



    
    
