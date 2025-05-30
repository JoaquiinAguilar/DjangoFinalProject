from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Usuario, Direccion

class UsuarioCreationForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ('nombre', 'apellidos', 'email', 'telefono', 'password1', 'password2')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personalizamos los campos
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class UsuarioUpdateForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ('nombre', 'apellidos', 'telefono')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'})
    )

class DireccionForm(forms.ModelForm):
    class Meta:
        model = Direccion
        fields = [
            'nombre', 'apellidos', 'telefono', 'email', 'calle', 
            'numero_ext', 'numero_int', 'colonia', 'ciudad', 'estado', 'codigo_postal'
        ]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})