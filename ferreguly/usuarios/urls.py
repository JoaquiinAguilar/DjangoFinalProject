from django.urls import path
from . import views

urlpatterns = [
    # URLs para usuarios
    path('registro/', views.RegistroUsuarioView.as_view(), name='registro'),
    path('login/', views.LoginUsuarioView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('perfil/', views.PerfilUsuarioView.as_view(), name='perfil'),
    
    # URLs para direcciones
    path('direcciones/', views.DireccionListView.as_view(), name='direcciones_lista'),
    path('direcciones/crear/', views.DireccionCreateView.as_view(), name='direccion_crear'),
    path('direcciones/editar/<int:pk>/', views.DireccionUpdateView.as_view(), name='direccion_editar'),
    path('direcciones/eliminar/<int:pk>/', views.DireccionDeleteView.as_view(), name='direccion_eliminar'),
    
    # URLs para administración de usuarios
    path('admin/usuarios/', views.UsuarioListView.as_view(), name='usuarios_admin_lista'),
    path('admin/usuarios/<int:pk>/', views.UsuarioDetailView.as_view(), name='usuario_admin_detalle'),
    path('admin/usuarios/editar/<int:pk>/', views.UsuarioUpdateAdminView.as_view(), name='usuario_admin_editar'),
]