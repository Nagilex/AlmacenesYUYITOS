from django.contrib import admin
from .models import (
    Proveedor, CategoriaProducto, Producto, Cliente, 
    Venta, DetalleVenta, Abono, OrdenPedido, 
    DetalleOrdenPedido, RecepcionProducto, DetalleRecepcion
)

@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'rut', 'telefono', 'rubro']
    search_fields = ['nombre', 'rut']

@admin.register(CategoriaProducto)
class CategoriaProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'codigo']

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nombre', 'precio', 'stock', 'proveedor']
    list_filter = ['categoria', 'proveedor']
    search_fields = ['codigo', 'nombre']

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'rut', 'deuda_actual', 'estado']
    list_filter = ['estado']
    search_fields = ['nombre', 'rut']

class DetalleVentaInline(admin.TabularInline):
    model = DetalleVenta
    extra = 0

@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ['numero_boleta', 'fecha', 'vendedor', 'tipo_pago', 'total']
    list_filter = ['tipo_pago', 'fecha']
    inlines = [DetalleVentaInline]

@admin.register(Abono)
class AbonoAdmin(admin.ModelAdmin):
    list_display = ['cliente', 'monto', 'fecha']
    list_filter = ['fecha']

@admin.register(OrdenPedido)
class OrdenPedidoAdmin(admin.ModelAdmin):
    list_display = ['id', 'proveedor', 'fecha']

@admin.register(RecepcionProducto)
class RecepcionProductoAdmin(admin.ModelAdmin):
    list_display = ['id', 'orden', 'fecha_recepcion']
