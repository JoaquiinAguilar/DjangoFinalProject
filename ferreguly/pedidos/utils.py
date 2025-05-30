from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse

from usuarios.models import Direccion

def verificar_direcciones(request):
    """
    Verifica si el usuario tiene direcciones registradas.
    Retorna True si tiene direcciones, False si no tiene.
    Si no tiene direcciones, redirige a la página de crear dirección.
    """
    tiene_direcciones = Direccion.objects.filter(id_usuario=request.user).exists()
    
    if not tiene_direcciones:
        messages.warning(
            request, 
            'No tienes direcciones registradas. Por favor, agrega una dirección para continuar con tu pedido.'
        )
        return False
        
    return True