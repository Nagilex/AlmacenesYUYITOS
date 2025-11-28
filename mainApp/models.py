from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Proveedor(models.Model):
    nombre = models.CharField(max_length=200)
    rut = models.CharField(max_length=12, unique=True)
    contacto = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    direccion = models.TextField()
    rubro = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "Proveedores"


class CategoriaProducto(models.Model):
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=3, unique=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "Categorías de Productos"


class Producto(models.Model):
    codigo = models.CharField(max_length=17, unique=True)
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT)
    categoria = models.ForeignKey(CategoriaProducto, on_delete=models.PROTECT)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    fecha_vencimiento = models.DateField(null=True, blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"

    class Meta:
        verbose_name_plural = "Productos"


class Cliente(models.Model):
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
    ]

    nombre = models.CharField(max_length=200)
    rut = models.CharField(max_length=12, unique=True)
    telefono = models.CharField(max_length=15)
    direccion = models.TextField()
    email = models.EmailField(blank=True)
    limite_credito = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    deuda_actual = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='activo')
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} - {self.rut}"

    class Meta:
        verbose_name_plural = "Clientes"


class Venta(models.Model):
    TIPO_PAGO_CHOICES = [
        ('contado', 'Contado'),
        ('credito', 'Crédito'),
    ]

    numero_boleta = models.CharField(max_length=10, unique=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, null=True, blank=True)
    vendedor = models.ForeignKey(User, on_delete=models.PROTECT)
    tipo_pago = models.CharField(max_length=10, choices=TIPO_PAGO_CHOICES)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(default=timezone.now)
    estado_credito = models.CharField(
        max_length=20,
        choices=[("PENDIENTE", "PENDIENTE"), ("CANCELADA", "CANCELADA")],
        default="PENDIENTE"
    )

    def __str__(self):
        return f"Boleta {self.numero_boleta} - ${self.total}"

    class Meta:
        verbose_name_plural = "Ventas"
        ordering = ['-fecha']

class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        self.subtotal = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.producto.nombre} x{self.cantidad}"


class Abono(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='abonos')
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(default=timezone.now)
    observaciones = models.TextField(blank=True)

    def __str__(self):
        return f"Abono {self.cliente.nombre} - ${self.monto}"

    class Meta:
        verbose_name_plural = "Abonos"
        ordering = ['-fecha']

class OrdenPedido(models.Model):
    proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT)
    fecha = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Orden #{self.id} – {self.proveedor.nombre}"

    class Meta:
        verbose_name_plural = "Órdenes de Pedido"


class DetalleOrdenPedido(models.Model):
    orden = models.ForeignKey(OrdenPedido, on_delete=models.CASCADE, related_name="detalles")
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad = models.IntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def subtotal(self):
        return self.cantidad * self.precio

    def __str__(self):
        return f"{self.producto.nombre} ({self.cantidad} u.)"


class RecepcionProducto(models.Model):
    orden = models.ForeignKey(OrdenPedido, on_delete=models.PROTECT)
    fecha_recepcion = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Recepción Orden #{self.orden.id}"

    class Meta:
        verbose_name_plural = "Recepciones"


class DetalleRecepcion(models.Model):
    recepcion = models.ForeignKey(RecepcionProducto, on_delete=models.CASCADE, related_name="detalles")
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad_recibida = models.IntegerField()

    def __str__(self):
        return f"{self.producto.nombre} recibidos: {self.cantidad_recibida}"


