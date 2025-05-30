# Ferreguly - Tienda de Ferretería Online

Ferreguly es un proyecto de Django que implementa una tienda online para una ferretería. Permite a los usuarios navegar por un catálogo de productos, agregar productos al carrito y realizar pedidos.

## Características

- **Catálogo de productos** organizados por categorías y marcas
- **Carrito de compras** para agregar y gestionar productos
- **Sistema de usuarios** con registro e inicio de sesión
- **Gestión de direcciones** para envíos
- **Procesamiento de pedidos**
- **Panel de administración** para gestionar productos, categorías, marcas y pedidos

## Requisitos

- Python 3.8 o superior
- Django 4.2
- Pillow (para manejo de imágenes)

## Instalación

1. Clona el repositorio o descarga los archivos
```
git clone https://github.com/JoaquiinAguilar/DjangoFinalProject.git
```

2. Crea un entorno virtual:
```
python -m venv venv
```

3. Activa el entorno virtual:
   - En Windows:
   ```
   venv\Scripts\activate
   ```
   - En macOS/Linux:
   ```
   source venv/bin/activate
   ```

4. Entrar a la carpeta raiz:
```
cd ferreguly
```

5. Instala las dependencias:
```
pip install -r requirements.txt
```

6. Realiza las migraciones:
```
python manage.py makemigrations
python manage.py migrate
```

7. Crea un superusuario:
```
python manage.py createsuperuser
```

8. Inicia el servidor:
```
python manage.py runserver
```

9. Enjoy!

## Estructura del Proyecto

- **usuarios**: Gestión de usuarios y direcciones
- **productos**: Gestión de productos, categorías y marcas
- **pedidos**: Gestión de carrito de compras y pedidos

## Cómo usar

### Para clientes:

1. Regístrate en la plataforma
2. Navega por el catálogo de productos
3. Agrega productos al carrito
4. Gestiona tu carrito (actualiza cantidades o elimina productos)
5. Finaliza tu compra proporcionando una dirección de envío
6. Consulta tus pedidos anteriores

### Para administradores:

1. Accede con una cuenta de administrador
2. Gestiona productos, categorías y marcas
3. Visualiza y actualiza el estado de los pedidos
4. Administra usuarios

