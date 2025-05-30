from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from productos.views import CatalogoView
from .views import HomeView  # Importar la vista de inicio personalizada

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # URL principal con la vista personalizada
    path('', HomeView.as_view(), name='inicio'),
    
    # Incluir las URLs de las aplicaciones
    path('usuarios/', include('usuarios.urls')),
    path('productos/', include('productos.urls')),
    path('pedidos/', include('pedidos.urls')),
]

# Configuración para servir archivos estáticos y media durante desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)