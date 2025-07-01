# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class ApiCliente(models.Model):
    cedulacliente = models.PositiveIntegerField(db_column='cedulaCliente', unique=True)  # Field name made lowercase.
    nombrecliente = models.CharField(db_column='nombreCliente', max_length=100)  # Field name made lowercase.
    direccioncliente = models.CharField(db_column='direccionCliente', max_length=255)  # Field name made lowercase.
    telefonocliente = models.CharField(db_column='telefonoCliente', max_length=100)  # Field name made lowercase.
    estado = models.CharField(max_length=3)

    class Meta:
        managed = False
        db_table = 'api_cliente'


class ApiDetalleventa(models.Model):
    nombrecliente = models.CharField(db_column='nombreCliente', max_length=100)  # Field name made lowercase.
    cedulacliente = models.PositiveIntegerField(db_column='cedulaCliente')  # Field name made lowercase.
    ventadetalle = models.OneToOneField('ApiVenta', models.DO_NOTHING, db_column='ventaDetalle_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'api_detalleventa'


class ApiDetalleventaproducto(models.Model):
    cantidad = models.PositiveIntegerField()
    producto = models.ForeignKey('ApiProducto', models.DO_NOTHING)
    venta = models.ForeignKey('ApiVenta', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'api_detalleventaproducto'


class ApiDetalleventaservicio(models.Model):
    cantidad = models.PositiveIntegerField()
    servicio = models.ForeignKey('ApiServicio', models.DO_NOTHING)
    venta = models.ForeignKey('ApiVenta', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'api_detalleventaservicio'


class ApiEmpleado(models.Model):
    nombreempleado = models.CharField(db_column='nombreEmpleado', max_length=100)  # Field name made lowercase.
    cedulaempleado = models.PositiveIntegerField(db_column='cedulaEmpleado', unique=True)  # Field name made lowercase.
    direccionempleado = models.CharField(db_column='direccionEmpleado', max_length=150)  # Field name made lowercase.
    telefonoempleado = models.CharField(db_column='telefonoEmpleado', max_length=100)  # Field name made lowercase.
    emailempleado = models.CharField(db_column='emailEmpleado', max_length=250)  # Field name made lowercase.
    nivelautorizacion = models.CharField(db_column='nivelAutorizacion', max_length=5)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'api_empleado'


class ApiProducto(models.Model):
    nombreproducto = models.CharField(db_column='nombreProducto', max_length=100)  # Field name made lowercase.
    codigoproducto = models.PositiveIntegerField(db_column='codigoProducto', unique=True)  # Field name made lowercase.
    stock = models.PositiveIntegerField()
    precioproducto = models.DecimalField(db_column='precioProducto', max_digits=10, decimal_places=5)  # Field name made lowercase. max_digits and decimal_places have been guessed, as this database handles decimal fields as float

    class Meta:
        managed = False
        db_table = 'api_producto'


class ApiServicio(models.Model):
    codigoservicio = models.PositiveBigIntegerField(db_column='codigoServicio', unique=True)  # Field name made lowercase.
    precioservicio = models.DecimalField(db_column='precioServicio', max_digits=10, decimal_places=5)  # Field name made lowercase. max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    nombreservicio = models.CharField(db_column='nombreServicio', max_length=100)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'api_servicio'


class ApiVenta(models.Model):
    fecha = models.DateTimeField()
    estadoventa = models.CharField(db_column='estadoVenta', max_length=4)  # Field name made lowercase.
    idcliente = models.ForeignKey(ApiCliente, models.DO_NOTHING, db_column='idCliente_id', blank=True, null=True)  # Field name made lowercase.
    idempleado = models.ForeignKey(ApiEmpleado, models.DO_NOTHING, db_column='idEmpleado_id', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'api_venta'


