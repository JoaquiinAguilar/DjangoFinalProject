from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q

from .models import Categoria, Marca, Producto
from .forms import CategoriaForm, MarcaForm, ProductoForm


# Vistas para el Catálogo de Productos (Usuario Final)
class CatalogoView(ListView):
    model = Producto
    template_name = 'productos/catalogo.html'
    context_object_name = 'productos'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Producto.objects.filter(activo=True)
        
        # Filtrado por categoría
        categoria_id = self.request.GET.get('categoria')
        if categoria_id:
            queryset = queryset.filter(id_categoria_id=categoria_id)
            
        # Filtrado por marca
        marca_id = self.request.GET.get('marca')
        if marca_id:
            queryset = queryset.filter(id_marca_id=marca_id)
            
        # Búsqueda por nombre
        busqueda = self.request.GET.get('busqueda')
        if busqueda:
            queryset = queryset.filter(
                Q(nombre__icontains=busqueda) | 
                Q(descripcion__icontains=busqueda)
            )
            
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.filter(activo=True)
        context['marcas'] = Marca.objects.filter(activo=True)
        return context

class ProductoDetailView(DetailView):
    model = Producto
    template_name = 'productos/detalle.html'
    context_object_name = 'producto'
    
    def get_queryset(self):
        return Producto.objects.filter(activo=True)

# Vistas CRUD para Categoría (Admin)
class CategoriaListView(LoginRequiredMixin, ListView):
    model = Categoria
    template_name = 'productos/admin/categorias/lista.html'
    context_object_name = 'categorias'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.tipo_usuario == 'administrador':
            messages.error(request, 'No tienes permisos para acceder a esta página')
            return redirect('inicio')
        return super().dispatch(request, *args, **kwargs)

class CategoriaCreateView(LoginRequiredMixin, CreateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'productos/admin/categorias/crear.html'
    success_url = reverse_lazy('categorias_lista')
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.tipo_usuario == 'administrador':
            messages.error(request, 'No tienes permisos para acceder a esta página')
            return redirect('inicio')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        messages.success(self.request, 'Categoría creada correctamente')
        return super().form_valid(form)

class CategoriaUpdateView(LoginRequiredMixin, UpdateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'productos/admin/categorias/editar.html'
    success_url = reverse_lazy('categorias_lista')
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.tipo_usuario == 'administrador':
            messages.error(request, 'No tienes permisos para acceder a esta página')
            return redirect('inicio')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        messages.success(self.request, 'Categoría actualizada correctamente')
        return super().form_valid(form)

class CategoriaDeleteView(LoginRequiredMixin, DeleteView):
    model = Categoria
    template_name = 'productos/admin/categorias/eliminar.html'
    success_url = reverse_lazy('categorias_lista')
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.tipo_usuario == 'administrador':
            messages.error(request, 'No tienes permisos para acceder a esta página')
            return redirect('inicio')
        return super().dispatch(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Categoría eliminada correctamente')
        return super().delete(request, *args, **kwargs)

# Vistas CRUD para Marca (Admin)
class MarcaListView(LoginRequiredMixin, ListView):
    model = Marca
    template_name = 'productos/admin/marcas/lista.html'
    context_object_name = 'marcas'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.tipo_usuario == 'administrador':
            messages.error(request, 'No tienes permisos para acceder a esta página')
            return redirect('inicio')
        return super().dispatch(request, *args, **kwargs)

class MarcaCreateView(LoginRequiredMixin, CreateView):
    model = Marca
    form_class = MarcaForm
    template_name = 'productos/admin/marcas/crear.html'
    success_url = reverse_lazy('marcas_lista')
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.tipo_usuario == 'administrador':
            messages.error(request, 'No tienes permisos para acceder a esta página')
            return redirect('inicio')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        messages.success(self.request, 'Marca creada correctamente')
        return super().form_valid(form)

class MarcaUpdateView(LoginRequiredMixin, UpdateView):
    model = Marca
    form_class = MarcaForm
    template_name = 'productos/admin/marcas/editar.html'
    success_url = reverse_lazy('marcas_lista')
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.tipo_usuario == 'administrador':
            messages.error(request, 'No tienes permisos para acceder a esta página')
            return redirect('inicio')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        messages.success(self.request, 'Marca actualizada correctamente')
        return super().form_valid(form)

class MarcaDeleteView(LoginRequiredMixin, DeleteView):
    model = Marca
    template_name = 'productos/admin/marcas/eliminar.html'
    success_url = reverse_lazy('marcas_lista')
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.tipo_usuario == 'administrador':
            messages.error(request, 'No tienes permisos para acceder a esta página')
            return redirect('inicio')
        return super().dispatch(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Marca eliminada correctamente')
        return super().delete(request, *args, **kwargs)

# Vistas CRUD para Producto (Admin)
class ProductoListView(LoginRequiredMixin, ListView):
    model = Producto
    template_name = 'productos/admin/productos/lista.html'
    context_object_name = 'productos'
    paginate_by = 10
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.tipo_usuario == 'administrador':
            messages.error(request, 'No tienes permisos para acceder a esta página')
            return redirect('inicio')
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        queryset = Producto.objects.all()
        
        # Filtrado por categoría
        categoria_id = self.request.GET.get('categoria')
        if categoria_id:
            queryset = queryset.filter(id_categoria_id=categoria_id)
            
        # Filtrado por marca
        marca_id = self.request.GET.get('marca')
        if marca_id:
            queryset = queryset.filter(id_marca_id=marca_id)
            
        # Búsqueda por nombre o descripción
        busqueda = self.request.GET.get('busqueda')
        if busqueda:
            queryset = queryset.filter(
                Q(nombre__icontains=busqueda) | 
                Q(descripcion__icontains=busqueda)
            )
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Agregar categorías y marcas al contexto para los filtros
        context['categorias'] = Categoria.objects.all()
        context['marcas'] = Marca.objects.all()
        return context

class ProductoCreateView(LoginRequiredMixin, CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'productos/admin/productos/crear.html'
    success_url = reverse_lazy('productos_lista')
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.tipo_usuario == 'administrador':
            messages.error(request, 'No tienes permisos para acceder a esta página')
            return redirect('inicio')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        messages.success(self.request, 'Producto creado correctamente')
        return super().form_valid(form)

class ProductoUpdateView(LoginRequiredMixin, UpdateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'productos/admin/productos/editar.html'
    success_url = reverse_lazy('productos_lista')
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.tipo_usuario == 'administrador':
            messages.error(request, 'No tienes permisos para acceder a esta página')
            return redirect('inicio')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        messages.success(self.request, 'Producto actualizado correctamente')
        return super().form_valid(form)

class ProductoDeleteView(LoginRequiredMixin, DeleteView):
    model = Producto
    template_name = 'productos/admin/productos/eliminar.html'
    success_url = reverse_lazy('productos_lista')
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.tipo_usuario == 'administrador':
            messages.error(request, 'No tienes permisos para acceder a esta página')
            return redirect('inicio')
        return super().dispatch(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Producto eliminado correctamente')
        return super().delete(request, *args, **kwargs)