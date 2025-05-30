from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.contrib import messages

from .models import Usuario, Direccion
from .forms import UsuarioCreationForm, UsuarioUpdateForm, LoginForm, DireccionForm

# Vistas para Usuario
class RegistroUsuarioView(CreateView):
    model = Usuario
    form_class = UsuarioCreationForm
    template_name = 'usuarios/registro.html'
    success_url = reverse_lazy('login')
    
    def form_valid(self, form):
        messages.success(self.request, 'Usuario registrado correctamente. Ahora puedes iniciar sesión.')
        return super().form_valid(form)

class LoginUsuarioView(LoginView):
    template_name = 'usuarios/login.html'
    form_class = LoginForm
    
    def get_success_url(self):
        return reverse_lazy('inicio')

def logout_view(request):
    logout(request)
    messages.success(request, 'Has cerrado sesión correctamente')
    return redirect('inicio')

class PerfilUsuarioView(LoginRequiredMixin, UpdateView):
    model = Usuario
    form_class = UsuarioUpdateForm
    template_name = 'usuarios/perfil.html'
    success_url = reverse_lazy('perfil')
    
    def get_object(self):
        return self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, 'Perfil actualizado correctamente')
        return super().form_valid(form)

# Vistas para Direcciones
class DireccionListView(LoginRequiredMixin, ListView):
    model = Direccion
    template_name = 'usuarios/direcciones/lista.html'
    context_object_name = 'direcciones'
    
    def get_queryset(self):
        return Direccion.objects.filter(id_usuario=self.request.user)

class DireccionCreateView(LoginRequiredMixin, CreateView):
    model = Direccion
    form_class = DireccionForm
    template_name = 'usuarios/direcciones/crear.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Verificar si viene de colocar pedido
        context['from_pedido'] = 'pedido' in self.request.GET.get('next', '')
        return context
    
    def form_valid(self, form):
        form.instance.id_usuario = self.request.user
        messages.success(self.request, 'Dirección creada correctamente')
        return super().form_valid(form)
    
    def get_success_url(self):
        # Si viene de la página de colocar pedido, regresar ahí
        next_url = self.request.GET.get('next')
        
        # Si es desde un pedido o si no tiene direcciones previas, redirigir a colocar_pedido
        if next_url and 'pedido' in next_url:
            return reverse_lazy('colocar_pedido')
        
        # Si vino desde otra página, verificar si tiene direcciones
        if not Direccion.objects.filter(id_usuario=self.request.user).exists():
            # Si esta es su primera dirección y estaba tratando de hacer un pedido
            if Carrito.objects.filter(id_usuario=self.request.user).exists(): # type: ignore
                return reverse_lazy('colocar_pedido')
                
        return reverse_lazy('direcciones_lista')
    

class DireccionUpdateView(LoginRequiredMixin, UpdateView):
    model = Direccion
    form_class = DireccionForm
    template_name = 'usuarios/direcciones/editar.html'
    success_url = reverse_lazy('direcciones_lista')
    
    def get_queryset(self):
        return Direccion.objects.filter(id_usuario=self.request.user)
    
    def form_valid(self, form):
        messages.success(self.request, 'Dirección actualizada correctamente')
        return super().form_valid(form)

class DireccionDeleteView(LoginRequiredMixin, DeleteView):
    model = Direccion
    template_name = 'usuarios/direcciones/eliminar.html'
    success_url = reverse_lazy('direcciones_lista')
    
    def get_queryset(self):
        return Direccion.objects.filter(id_usuario=self.request.user)
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Dirección eliminada correctamente')
        return super().delete(request, *args, **kwargs)

# Vistas CRUD para administradores
class UsuarioListView(LoginRequiredMixin, ListView):
    model = Usuario
    template_name = 'usuarios/admin/lista.html'
    context_object_name = 'usuarios'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.tipo_usuario == 'administrador':
            messages.error(request, 'No tienes permisos para acceder a esta página')
            return redirect('inicio')
        return super().dispatch(request, *args, **kwargs)

class UsuarioDetailView(LoginRequiredMixin, DetailView):
    model = Usuario
    template_name = 'usuarios/admin/detalle.html'
    context_object_name = 'usuario'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.tipo_usuario == 'administrador':
            messages.error(request, 'No tienes permisos para acceder a esta página')
            return redirect('inicio')
        return super().dispatch(request, *args, **kwargs)

class UsuarioUpdateAdminView(LoginRequiredMixin, UpdateView):
    model = Usuario
    template_name = 'usuarios/admin/editar.html'
    fields = ['nombre', 'apellidos', 'email', 'telefono', 'tipo_usuario', 'activo']
    success_url = reverse_lazy('usuarios_admin_lista')
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.tipo_usuario == 'administrador':
            messages.error(request, 'No tienes permisos para acceder a esta página')
            return redirect('inicio')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        messages.success(self.request, 'Usuario actualizado correctamente')
        return super().form_valid(form)