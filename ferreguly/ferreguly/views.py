from django.views.generic import TemplateView
from productos.models import Categoria, Producto

class HomeView(TemplateView):
    template_name = 'home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Obtener todas las categorías activas
        context['categorias'] = Categoria.objects.filter(activo=True)
        
        # Obtener productos destacados (los más recientes)
        context['productos_destacados'] = Producto.objects.filter(activo=True).order_by('-fecha_creacion')[:6]
        
        return context