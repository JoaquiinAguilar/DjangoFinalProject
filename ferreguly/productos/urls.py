from django.urls import path
from . import views

urlpatterns = [
    # URLs para catálogo (usuario final)
    path('', views.CatalogoView.as_view(), name='catalogo'),
    path('producto/<int:pk>/', views.ProductoDetailView.as_view(), name='producto_detalle'),
    
    # URLs para categorías (admin)
    path('admin/categorias/', views.CategoriaListView.as_view(), name='categorias_lista'),
    path('admin/categorias/crear/', views.CategoriaCreateView.as_view(), name='categoria_crear'),
    path('admin/categorias/editar/<int:pk>/', views.CategoriaUpdateView.as_view(), name='categoria_editar'),
    path('admin/categorias/eliminar/<int:pk>/', views.CategoriaDeleteView.as_view(), name='categoria_eliminar'),
    
    # URLs para marcas (admin)
    path('admin/marcas/', views.MarcaListView.as_view(), name='marcas_lista'),
    path('admin/marcas/crear/', views.MarcaCreateView.as_view(), name='marca_crear'),
    path('admin/marcas/editar/<int:pk>/', views.MarcaUpdateView.as_view(), name='marca_editar'),
    path('admin/marcas/eliminar/<int:pk>/', views.MarcaDeleteView.as_view(), name='marca_eliminar'),
    
    # URLs para productos (admin)
    path('admin/productos/', views.ProductoListView.as_view(), name='productos_lista'),
    path('admin/productos/crear/', views.ProductoCreateView.as_view(), name='producto_crear'),
    path('admin/productos/editar/<int:pk>/', views.ProductoUpdateView.as_view(), name='producto_editar'),
    path('admin/productos/eliminar/<int:pk>/', views.ProductoDeleteView.as_view(), name='producto_eliminar'),
]