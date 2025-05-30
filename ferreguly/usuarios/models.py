from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone

class UsuarioManager(BaseUserManager):
    def create_user(self, email, nombre, apellidos, contraseña=None, **extra_fields):
        if not email:
            raise ValueError('El Email es obligatorio')
        email = self.normalize_email(email)
        usuario = self.model(email=email, nombre=nombre, apellidos=apellidos, **extra_fields)
        usuario.set_password(contraseña)
        usuario.save(using=self._db)
        return usuario

    def create_superuser(self, email, nombre, apellidos, contraseña=None, **extra_fields):
        extra_fields.setdefault('tipo_usuario', 'administrador')
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        return self.create_user(email, nombre, apellidos, contraseña, **extra_fields)

class Usuario(AbstractBaseUser, PermissionsMixin):
    id_usuario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=35)
    apellidos = models.CharField(max_length=50)
    email = models.EmailField(max_length=45, unique=True)
    telefono = models.CharField(max_length=10, null=True, blank=True)
    tipo_usuario = models.CharField(
        max_length=15,
        choices=[('cliente', 'Cliente'), ('administrador', 'Administrador')],
        default='cliente'
    )
    fecha_registro = models.DateTimeField(default=timezone.now)
    activo = models.BooleanField(default=True)
    
    # Campos requeridos por Django para extender AbstractBaseUser
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombre', 'apellidos']
    
    objects = UsuarioManager()
    
    def __str__(self):
        return f"{self.nombre} {self.apellidos}"
    
    def get_full_name(self):
        return f"{self.nombre} {self.apellidos}"
    
    def get_short_name(self):
        return self.nombre
    
    class Meta:
        db_table = 'usuario'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

class Direccion(models.Model):
    id_direccion = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='direcciones')
    nombre = models.CharField(max_length=35)
    apellidos = models.CharField(max_length=50)
    telefono = models.CharField(max_length=10)
    email = models.EmailField(max_length=45)
    calle = models.CharField(max_length=80)
    numero_ext = models.CharField(max_length=10)
    numero_int = models.CharField(max_length=10, null=True, blank=True)
    colonia = models.CharField(max_length=60)
    ciudad = models.CharField(max_length=40)
    estado = models.CharField(max_length=30)
    codigo_postal = models.CharField(max_length=5)
    
    def __str__(self):
        return f"{self.calle} {self.numero_ext}, {self.colonia}, {self.ciudad}"
    
    class Meta:
        db_table = 'direccion'
        verbose_name = 'Dirección'
        verbose_name_plural = 'Direcciones'