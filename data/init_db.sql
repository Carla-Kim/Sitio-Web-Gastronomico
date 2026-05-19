CREATE DATABASE IF NOT EXISTS gastronomia_db;
USE gastronomia_db;

CREATE TABLE IF NOT EXISTS usuarios (
    usuario_id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    nombre_usuario VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(50) NOT NULL UNIQUE,
    contrasena VARCHAR(100) NOT NULL,
    rol VARCHAR(30) NOT NULL CHECK (rol IN ('cliente', 'admin')),
    estado VARCHAR(30)
        NOT NULL
        DEFAULT 'activo'
        CHECK (estado IN ('activo', 'inactivo'))
);

CREATE TABLE IF NOT EXISTS menus (
    menu_id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT NULL,
    precio DECIMAL(10, 2) NOT NULL,
    categoria VARCHAR(30)
        NOT NULL
        CHECK (categoria IN ('plato', 'bebida', 'postre')),
    disponible BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS reservas (
    reserva_id INT PRIMARY KEY AUTO_INCREMENT,
    usuario_id INT NULL,
    fecha DATE NOT NULL,
    hora TIME NOT NULL,
    comensales INT NOT NULL CHECK (comensales > 0),
    estado VARCHAR(30)
        NOT NULL
        DEFAULT 'reservada'
        CHECK (estado IN ('reservada', 'cancelada', 'finalizada')),
    
    FOREIGN KEY (usuario_id)
        REFERENCES usuarios(usuario_id)
        ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS resenas (
    resena_id INT PRIMARY KEY AUTO_INCREMENT,
    usuario_id INT NULL,
    reserva_id INT NOT NULL UNIQUE,
    puntuacion_ambiente INT
        NOT NULL
        CHECK (puntuacion_ambiente BETWEEN 1 AND 5),
    puntuacion_servicio INT
        NOT NULL
        CHECK (puntuacion_servicio BETWEEN 1 AND 5),
    puntuacion_comida INT
        NOT NULL
        CHECK (puntuacion_comida BETWEEN 1 AND 5),
    comentario TEXT NULL,
    fecha DATE NOT NULL,

    FOREIGN KEY (usuario_id)
        REFERENCES usuarios(usuario_id)
        ON DELETE RESTRICT,
    FOREIGN KEY (reserva_id)
        REFERENCES reservas(reserva_id)
        ON DELETE CASCADE
);
