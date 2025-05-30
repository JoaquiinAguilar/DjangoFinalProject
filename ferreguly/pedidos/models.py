from django.db import models
from django.utils import timezone
from usuarios.models import Usuario, Direccion
from productos.models import Producto

class Pedido(models.Model):
    ESTADOS_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('pagado', 'Pagado'),
        ('enviado', 'Enviado'),
        ('entregado', 'Entregado'),
        ('cancelado', 'Cancelado'),
    ]
    
    id_pedido = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.RESTRICT, related_name='pedidos')
    id_direccion_envio = models.ForeignKey(
        Direccion, 
        on_delete=models.SET_NULL, 
        related_name='pedidos',
        null=True, 
        blank=True
    )
    fecha_pedido = models.DateTimeField(default=timezone.now)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=15, choices=ESTADOS_CHOICES, default='pendiente')
    
    def __str__(self):
        return f"Pedido #{self.id_pedido} - {self.id_usuario.get_full_name()}"
    
    class Meta:
        db_table = 'pedido'
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'
        indexes = [
            models.Index(fields=['id_usuario'], name='idx_pedido_usuario'),
            models.Index(fields=['fecha_pedido'], name='idx_pedido_fecha'),
        ]

class DetallePedido(models.Model):
    id_detalle = models.AutoField(primary_key=True)
    id_pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='detalles')
    id_producto = models.ForeignKey(Producto, on_delete=models.RESTRICT, related_name='detalles_pedido')
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"Detalle #{self.id_detalle} - Pedido #{self.id_pedido.id_pedido}"
    
    def save(self, *args, **kwargs):
        self.subtotal = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)
    
    class Meta:
        db_table = 'detalle_pedido'
        verbose_name = 'Detalle de pedido'
        verbose_name_plural = 'Detalles de pedidos'

class Carrito(models.Model):
    id_carrito = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='carrito')
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='carrito_items')
    cantidad = models.IntegerField(default=1)
    fecha_agregado = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'carrito'
        verbose_name = 'Carrito'
        verbose_name_plural = 'Carritos'
        unique_together = ('id_usuario', 'id_producto')
        indexes = [
            models.Index(fields=['id_usuario'], name='idx_carrito_usuario'),
        ]
    
    def __str__(self):
        return f"{self.id_usuario.get_full_name()} - {self.id_producto.nombre}"
    
    @property
    def subtotal(self):
        return self.cantidad * self.id_producto.precio