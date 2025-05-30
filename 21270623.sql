
DROP DATABASE IF EXISTS ferreguly;
CREATE DATABASE ferreguly CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE ferreguly;

SET FOREIGN_KEY_CHECKS = 0;

CREATE TABLE usuario (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(35) NOT NULL,
    apellidos VARCHAR(50) NOT NULL,
    email VARCHAR(45) UNIQUE NOT NULL,
    contraseña VARCHAR(128) NOT NULL,
    telefono VARCHAR(10),
    tipo_usuario VARCHAR(20) NOT NULL DEFAULT 'cliente',
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
    activo BOOLEAN DEFAULT TRUE,
    CONSTRAINT chk_tipo_usuario CHECK (tipo_usuario IN ('cliente', 'administrador'))
) ENGINE=InnoDB;

CREATE TABLE direccion (
    id_direccion INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    nombre VARCHAR(35) NOT NULL,
    apellidos VARCHAR(50) NOT NULL,
    telefono VARCHAR(10) NOT NULL,
    email VARCHAR(45) NOT NULL,
    calle VARCHAR(80) NOT NULL,
    numero_ext VARCHAR(10) NOT NULL,
    numero_int VARCHAR(10),
    colonia VARCHAR(60) NOT NULL,
    ciudad VARCHAR(40) NOT NULL,
    estado VARCHAR(30) NOT NULL,
    codigo_postal VARCHAR(5) NOT NULL,
    CONSTRAINT fk_usuario_direccion FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE categoria (
    id_categoria INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(35) NOT NULL,
    descripcion TEXT,
    activo BOOLEAN DEFAULT TRUE
) ENGINE=InnoDB;

CREATE TABLE marca (
    id_marca INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(35) NOT NULL,
    activo BOOLEAN DEFAULT TRUE
) ENGINE=InnoDB;

CREATE TABLE producto (
    id_producto INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT NOT NULL,
    id_categoria INT NOT NULL,
    id_marca INT NOT NULL,
    precio DECIMAL(10,2) NOT NULL CHECK(precio >= 0),
    stock INT NOT NULL DEFAULT 0 CHECK(stock >= 0),
    imagen VARCHAR(200),
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_pertenece FOREIGN KEY (id_categoria) REFERENCES categoria(id_categoria) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_marca_tiene FOREIGN KEY (id_marca) REFERENCES marca(id_marca) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB;


CREATE TABLE pedido (
    id_pedido INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    id_direccion_envio INT,
    fecha_pedido DATETIME DEFAULT CURRENT_TIMESTAMP,
    subtotal DECIMAL(10,2) NOT NULL CHECK(subtotal >= 0),
    total DECIMAL(10,2) NOT NULL CHECK(total >= 0),
    estado VARCHAR(20) DEFAULT 'pendiente',
    CONSTRAINT chk_estado_pedido CHECK (estado IN ('pendiente', 'pagado', 'enviado', 'entregado', 'cancelado')),
    CONSTRAINT fk_compra FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_usa FOREIGN KEY (id_direccion_envio) REFERENCES direccion(id_direccion) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE detalle_pedido (
    id_detalle INT AUTO_INCREMENT PRIMARY KEY,
    id_pedido INT NOT NULL,
    id_producto INT NOT NULL,
    cantidad INT NOT NULL CHECK(cantidad > 0),
    precio_unitario DECIMAL(10,2) NOT NULL CHECK(precio_unitario >= 0),
    subtotal DECIMAL(10,2) NOT NULL CHECK(subtotal >= 0),
    CONSTRAINT fk_contiene FOREIGN KEY (id_pedido) REFERENCES pedido(id_pedido) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_refiere FOREIGN KEY (id_producto) REFERENCES producto(id_producto) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE carrito (
    id_carrito INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    id_producto INT NOT NULL,
    cantidad INT NOT NULL DEFAULT 1 CHECK(cantidad > 0),
    fecha_agregado DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_usuario_tiene FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_producto_contiene FOREIGN KEY (id_producto) REFERENCES producto(id_producto) ON DELETE CASCADE ON UPDATE CASCADE,
    UNIQUE KEY unq_usuario_producto (id_usuario, id_producto)
) ENGINE=InnoDB;

CREATE INDEX idx_producto_categoria ON producto(id_categoria);
CREATE INDEX idx_producto_marca ON producto(id_marca);
CREATE INDEX idx_pedido_usuario ON pedido(id_usuario);
CREATE INDEX idx_pedido_fecha ON pedido(fecha_pedido);
CREATE INDEX idx_carrito_usuario ON carrito(id_usuario);
CREATE INDEX idx_direccion_usuario ON direccion(id_usuario);

SET FOREIGN_KEY_CHECKS = 1;
