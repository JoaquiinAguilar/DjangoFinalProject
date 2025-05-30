from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db import transaction
from django.db.models import Sum, F
from decimal import Decimal

from .models import Pedido, DetallePedido, Carrito
from usuarios.models import Direccion
from productos.models import Producto
from .forms import PedidoForm, CarritoAddForm, CarritoUpdateForm

# Vistas para el Carrito
@login_required
def carrito_lista(request):
    items = Carrito.objects.filter(id_usuario=request.user).select_related('id_producto')
    total = sum(item.subtotal for item in items)
    
    return render(request, 'pedidos/carrito.html', {
        'items': items,
        'total': total
    })

@login_required
def carrito_add(request, producto_id):
    producto = get_object_or_404(Producto, id_producto=producto_id, activo=True)
    
    # Verificar stock
    if producto.stock <= 0:
        messages.error(request, f'Lo sentimos, {producto.nombre} no tiene stock disponible.')
        return redirect('catalogo')
    
    if request.method == 'POST':
        form = CarritoAddForm(request.POST)
        if form.is_valid():
            cantidad = form.cleaned_data['cantidad']
            
            # Verificar que la cantidad no supere el stock
            if cantidad > producto.stock:
                messages.error(request, f'La cantidad solicitada supera el stock disponible ({producto.stock}).')
                return redirect('producto_detalle', pk=producto_id)
            
            # Actualizar o crear el item en el carrito
            carrito_item, created = Carrito.objects.get_or_create(
                id_usuario=request.user,
                id_producto=producto,
                defaults={'cantidad': cantidad}
            )
            
            if not created:
                # Si ya existe, actualizar la cantidad
                nueva_cantidad = carrito_item.cantidad + cantidad
                if nueva_cantidad > producto.stock:
                    messages.error(request, f'La cantidad total en el carrito supera el stock disponible ({producto.stock}).')
                    return redirect('producto_detalle', pk=producto_id)
                
                carrito_item.cantidad = nueva_cantidad
                carrito_item.save()
            
            messages.success(request, f'{producto.nombre} agregado al carrito.')
            return redirect('carrito_lista')
    else:
        form = CarritoAddForm(initial={'id_producto': producto_id})
    
    return render(request, 'pedidos/agregar_carrito.html', {
        'form': form,
        'producto': producto
    })

@login_required
def carrito_update(request, item_id):
    item = get_object_or_404(Carrito, id_carrito=item_id, id_usuario=request.user)
    producto = item.id_producto
    
    if request.method == 'POST':
        form = CarritoUpdateForm(request.POST, instance=item)
        if form.is_valid():
            cantidad = form.cleaned_data['cantidad']
            
            # Verificar stock
            if cantidad > producto.stock:
                messages.error(request, f'La cantidad solicitada supera el stock disponible ({producto.stock}).')
            else:
                form.save()
                messages.success(request, 'Carrito actualizado correctamente.')
            
            return redirect('carrito_lista')
    else:
        form = CarritoUpdateForm(instance=item)
    
    return render(request, 'pedidos/actualizar_carrito.html', {
        'form': form,
        'item': item
    })

@login_required
def carrito_remove(request, item_id):
    item = get_object_or_404(Carrito, id_carrito=item_id, id_usuario=request.user)
    
    if request.method == 'POST':
        item.delete()
        messages.success(request, 'Producto eliminado del carrito.')
        return redirect('carrito_lista')
    
    return render(request, 'pedidos/eliminar_carrito.html', {'item': item})

# Vista para colocar pedido
@login_required
def colocar_pedido(request):
    # Verificar que el carrito no esté vacío
    carrito_items = Carrito.objects.filter(id_usuario=request.user).select_related('id_producto')
    
    if not carrito_items.exists():
        messages.error(request, 'Tu carrito está vacío.')
        return redirect('carrito_lista')
    
    # Verificar que todos los productos tengan stock suficiente
    for item in carrito_items:
        if item.cantidad > item.id_producto.stock:
            messages.error(
                request, 
                f'La cantidad de "{item.id_producto.nombre}" supera el stock disponible ({item.id_producto.stock}).'
            )
            return redirect('carrito_lista')
    
    # Obtener las direcciones del usuario y verificar si tiene alguna
    direcciones = Direccion.objects.filter(id_usuario=request.user)
    tiene_direcciones = direcciones.exists()
    
    # Si no tiene direcciones, redirigir a la página de agregar dirección
    if not tiene_direcciones and request.method != 'POST':
        messages.warning(request, 'Necesitas agregar una dirección para completar tu pedido.')
        return redirect('direccion_crear')
    
    if request.method == 'POST':
        form = PedidoForm(request.user, request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    # Calcular totales
                    subtotal = sum(item.subtotal for item in carrito_items)
                    total = subtotal  # Aquí se podría agregar lógica para impuestos, envío, etc.
                    
                    # Crear pedido
                    pedido = Pedido(
                        id_usuario=request.user,
                        id_direccion_envio=form.cleaned_data['id_direccion_envio'],
                        subtotal=subtotal,
                        total=total,
                        estado='pendiente'
                    )
                    pedido.save()
                    
                    # Crear detalles del pedido
                    for item in carrito_items:
                        DetallePedido.objects.create(
                            id_pedido=pedido,
                            id_producto=item.id_producto,
                            cantidad=item.cantidad,
                            precio_unitario=item.id_producto.precio,
                            subtotal=item.subtotal
                        )
                        
                        # Actualizar stock del producto
                        producto = item.id_producto
                        producto.stock -= item.cantidad
                        producto.save()
                    
                    # Vaciar el carrito
                    carrito_items.delete()
                    
                    messages.success(request, f'¡Pedido #{pedido.id_pedido} creado correctamente!')
                    return redirect('pedido_detalle', pk=pedido.id_pedido)
            except Exception as e:
                messages.error(request, f'Error al procesar el pedido: {str(e)}')
    else:
        form = PedidoForm(request.user)
    
    # Calcular total del carrito
    total = sum(item.subtotal for item in carrito_items)
    
    return render(request, 'pedidos/colocar_pedido.html', {
        'form': form,
        'carrito_items': carrito_items,
        'total': total,
        'direcciones': direcciones,
        'tiene_direcciones': tiene_direcciones
    })

# Vistas para Pedidos (Cliente)
class PedidoListView(LoginRequiredMixin, ListView):
    model = Pedido
    template_name = 'pedidos/lista.html'
    context_object_name = 'pedidos'
    
    def get_queryset(self):
        return Pedido.objects.filter(id_usuario=self.request.user).order_by('-fecha_pedido')

class PedidoDetailView(LoginRequiredMixin, DetailView):
    model = Pedido
    template_name = 'pedidos/detalle.html'
    context_object_name = 'pedido'
    
    def get_queryset(self):
        return Pedido.objects.filter(id_usuario=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['detalles'] = self.object.detalles.all()
        return context

# Vistas CRUD para Pedidos (Admin)
class PedidoAdminListView(LoginRequiredMixin, ListView):
    model = Pedido
    template_name = 'pedidos/admin/lista.html'
    context_object_name = 'pedidos'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.tipo_usuario == 'administrador':
            messages.error(request, 'No tienes permisos para acceder a esta página')
            return redirect('inicio')
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        return Pedido.objects.all().order_by('-fecha_pedido')

class PedidoAdminDetailView(LoginRequiredMixin, DetailView):
    model = Pedido
    template_name = 'pedidos/admin/detalle.html'
    context_object_name = 'pedido'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.tipo_usuario == 'administrador':
            messages.error(request, 'No tienes permisos para acceder a esta página')
            return redirect('inicio')
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['detalles'] = self.object.detalles.all()
        return context

@login_required
def actualizar_estado_pedido(request, pk):
    if not request.user.tipo_usuario == 'administrador':
        messages.error(request, 'No tienes permisos para acceder a esta función')
        return redirect('inicio')
    
    pedido = get_object_or_404(Pedido, id_pedido=pk)
    
    if request.method == 'POST':
        nuevo_estado = request.POST.get('estado')
        if nuevo_estado in dict(Pedido.ESTADOS_CHOICES).keys():
            pedido.estado = nuevo_estado
            pedido.save()
            messages.success(request, f'Estado del pedido actualizado a: {nuevo_estado}')
        else:
            messages.error(request, 'Estado no válido')
        
        return redirect('pedido_admin_detalle', pk=pk)
    
    return render(request, 'pedidos/admin/actualizar_estado.html', {'pedido': pedido})