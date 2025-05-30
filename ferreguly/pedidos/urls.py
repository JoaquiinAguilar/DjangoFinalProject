from django.urls import path
from . import views

urlpatterns = [
    # URLs para carrito
    path('carrito/', views.carrito_lista, name='carrito_lista'),
    path('carrito/agregar/<int:producto_id>/', views.carrito_add, name='carrito_agregar'),
    path('carrito/actualizar/<int:item_id>/', views.carrito_update, name='carrito_actualizar'),
    path('carrito/eliminar/<int:item_id>/', views.carrito_remove, name='carrito_eliminar'),
    
    # URL para colocar pedido
    path('colocar-pedido/', views.colocar_pedido, name='colocar_pedido'),
    
    # URLs para pedidos (cliente)
    path('mis-pedidos/', views.PedidoListView.as_view(), name='pedidos_lista'),
    path('mis-pedidos/<int:pk>/', views.PedidoDetailView.as_view(), name='pedido_detalle'),
    
    # URLs para pedidos (admin)
    path('admin/pedidos/', views.PedidoAdminListView.as_view(), name='pedidos_admin_lista'),
    path('admin/pedidos/<int:pk>/', views.PedidoAdminDetailView.as_view(), name='pedido_admin_detalle'),
    path('admin/pedidos/<int:pk>/actualizar-estado/', views.actualizar_estado_pedido, name='pedido_actualizar_estado'),
]