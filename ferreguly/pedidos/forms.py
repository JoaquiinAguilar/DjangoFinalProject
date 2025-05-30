from django import forms
from .models import Pedido, Carrito
from usuarios.models import Direccion

class PedidoForm(forms.ModelForm):
    id_direccion_envio = forms.ModelChoiceField(
        queryset=Direccion.objects.none(),
        empty_label=None,  # Sin opción vacía
        required=True,
        widget=forms.RadioSelect()
    )
    
    class Meta:
        model = Pedido
        fields = ['id_direccion_envio']
        
    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['id_direccion_envio'].queryset = Direccion.objects.filter(id_usuario=user)
            
    def clean(self):
        cleaned_data = super().clean()
        direccion_envio = cleaned_data.get('id_direccion_envio')
        
        if not direccion_envio:
            raise forms.ValidationError('Debes seleccionar una dirección de envío.')
            
        return cleaned_data
    
    
class CarritoAddForm(forms.Form):
    cantidad = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'value': 1})
    )
    id_producto = forms.IntegerField(widget=forms.HiddenInput())

class CarritoUpdateForm(forms.ModelForm):
    class Meta:
        model = Carrito
        fields = ['cantidad']
        widgets = {
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': 1})
        }