CREATE DATABASE IF NOT EXISTS gastronomia_db;
USE gastronomia_db;

CREATE TABLE IF NOT EXISTS Usuarios (
    usuario_id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    nombre_usuario VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    contrasena VARCHAR(100) NOT NULL,
    rol VARCHAR(30) NOT NULL CHECK (rol IN ('cliente', 'admin')),
);

CREATE TABLE IF NOT EXISTS Categorias(
    categorias_id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL UNIQUE
)

CREATE TABLE IF NOT EXISTS Productos(
    producto_id INT PRIMARY KEY AUTO_INCREMENT,
    categorias_id INT FOREIGN KEY REFERENCES Categorias(categorias_id) ON DELETE RESTRICT,
    nombre VARCHAR(100) NOT NULL,
    precio DECIMAL(10, 2) NOT NULL CHECK (precio >= 0),
)

CREATE TABLE IF NOT EXISTS Reservas (
    reserva_id INT PRIMARY KEY AUTO_INCREMENT,
    fecha DATE NOT NULL,
    email VARCHAR(100) NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    DNI VARCHAR(20) NOT NULL,
    servicio_ID INT FOREIGN KEY REFERENCES Servicios(servicio_id) ON DELETE RESTRICT,
    telefono VARCHAR(20) NOT NULL,
    cantidad_personas INT NOT NULL CHECK (cantidad_personas > 0),
    estado VARCHAR(30)
        NOT NULL
        DEFAULT 'reservada'
        CHECK (estado IN ('reservada', 'cancelada', 'finalizada'))
);

CREATE TABLE IF NOT EXISTS Resenas (
    resena_id INT PRIMARY KEY AUTO_INCREMENT,
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

    FOREIGN KEY (reserva_id)
        REFERENCES Reservas(reserva_id)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Servicios(
    servicio_id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL UNIQUE,
)

CREATE TABLE IF NOT EXISTS Servicios_reserva(
    servicios_reserva_id INT PRIMARY KEY AUTO_INCREMENT,
    reserva_id INT NOT NULL,
    servicio_id INT NOT NULL,

    FOREIGN KEY (reserva_id)
        REFERENCES Reservas(reserva_id)
        ON DELETE CASCADE,
    FOREIGN KEY (servicio_id)
        REFERENCES Servicios(servicio_id)
        ON DELETE RESTRICT
)

CREATE TABLE IF NOT EXISTS Mesas(
    mesa_id INT PRIMARY KEY AUTO_INCREMENT,
    estado VARCHAR(20) NOT NULL DEFAULT 'desocupados' CHECK (estado IN ('ocupados', 'desocupados')),
    cantidad_personas INT NOT NULL CHECK (cantidad_personas > 0)
);

-- Insertamos la categoría inicial para que tu prueba de Postman no falle
INSERT INTO Categorias (categorias_id, nombre) VALUES (1, 'Platos Principales');