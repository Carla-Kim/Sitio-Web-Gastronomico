CREATE DATABASE IF NOT EXISTS gastronomia_db;
USE gastronomia_db;

CREATE TABLE IF NOT EXISTS Usuarios (
    usuario_id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    nombre_usuario VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    contrasena VARCHAR(255) NOT NULL,
    rol VARCHAR(30) NOT NULL CHECK (rol IN ('cliente', 'admin'))
);

CREATE TABLE IF NOT EXISTS Categorias (
    categorias_id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS Productos (
    producto_id INT PRIMARY KEY AUTO_INCREMENT,
    categorias_id INT NOT NULL,
    descripcion VARCHAR(300),
    nombre VARCHAR(100) NOT NULL,
    precio DECIMAL(10, 2) NOT NULL CHECK (precio >= 0),
    FOREIGN KEY (categorias_id) REFERENCES Categorias(categorias_id) ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS Servicios (
    servicio_id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS Reservas (
    reserva_id INT PRIMARY KEY AUTO_INCREMENT,
    fecha DATE NOT NULL,
    email VARCHAR(100) NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    DNI VARCHAR(12) NOT NULL,
    servicio_ID INT NOT NULL,
    telefono VARCHAR(20) NOT NULL,
    cantidad_personas INT NOT NULL CHECK (cantidad_personas > 0),
    estado VARCHAR(30) NOT NULL DEFAULT 'reservada' CHECK (estado IN ('reservada', 'cancelada', 'finalizada')),
    FOREIGN KEY (servicio_ID) REFERENCES Servicios(servicio_id) ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS Resenas (
    resena_id INT PRIMARY KEY AUTO_INCREMENT,
    reserva_id INT NOT NULL UNIQUE,
    puntuacion_ambiente INT NOT NULL CHECK (puntuacion_ambiente BETWEEN 1 AND 5),
    puntuacion_servicio INT NOT NULL CHECK (puntuacion_servicio BETWEEN 1 AND 5),
    puntuacion_comida INT NOT NULL CHECK (puntuacion_comida BETWEEN 1 AND 5),
    comentario TEXT NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (reserva_id) REFERENCES Reservas(reserva_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Servicios_reserva (
    servicios_reserva_id INT PRIMARY KEY AUTO_INCREMENT,
    reserva_id INT NOT NULL,
    servicio_id INT NOT NULL,
    FOREIGN KEY (reserva_id) REFERENCES Reservas(reserva_id) ON DELETE CASCADE,
    FOREIGN KEY (servicio_id) REFERENCES Servicios(servicio_id) ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS Mesas (
    mesa_id INT PRIMARY KEY AUTO_INCREMENT,
    estado VARCHAR(20) NOT NULL DEFAULT 'desocupada' CHECK (estado IN ('ocupada', 'desocupada')),
    cantidad_personas INT NOT NULL CHECK (cantidad_personas > 0)
);

-- =========================================================================
-- DATOS EJEMPLO PARA BASE DE DATOS
-- =========================================================================
INSERT IGNORE INTO Usuarios (usuario_id, nombre, apellido, nombre_usuario, email, contrasena, rol) VALUES 
(1, 'Kevin', 'La Rocca', 'kevin_dev', 'kevin@test.com', 'hashed_password_123', 'admin'),
(2, 'Carla', 'Kim', 'carla_admin', 'carla@test.com', 'hashed_password_456', 'admin'),
(3, 'Juan', 'Pérez', 'juan_comensal', 'juan.perez@gmail.com', 'hashed_user_789', 'cliente'),
(4, 'María', 'Gomez', 'maria_g', 'maria.gomez@hotmail.com', 'hashed_user_abc', 'cliente'),
(5, 'Carlos', 'Rodríguez', 'carlos_rod', 'carlos.rodriguez@gmail.com', 'hashed_user_def', 'cliente'),
(6, 'Ana', 'Martínez', 'ana_mar', 'ana.martinez@yahoo.com', 'hashed_user_ghi', 'cliente');

INSERT IGNORE INTO Categorias (categorias_id, nombre) VALUES 
(1, 'Entradas'),
(2, 'Platos Principales'),
(3, 'Postres'),
(4, 'Bebidas');

INSERT IGNORE INTO Productos (producto_id, categorias_id, descripcion, nombre, precio) VALUES 
-- Entradas
(1, 1, 'Empanada de carne cortada a cuchillo, frita', 'Empanada de Carne', 450.00),
(2, 1, 'Provoleta tradicional a la chapa con orégano y oliva', 'Provoleta Clásica', 1800.00),
(3, 1, 'Porción de papas fritas bastón crujientes', 'Papas Fritas Medianas', 1100.00),
(4, 1, 'Bastones de muzzarella rebozados acompañados de salsa pomodoro', 'Bastones de Muzzarella', 1500.00),

-- Platos Principales
(5, 2, 'Milanesa de ternera acompañada de papas fritas', 'Milanesa Clásica', 1250.00),
(6, 2, 'Bife de chorizo de 400g con guarnición a elección', 'Bife de Chorizo', 4200.00),
(7, 2, 'Ravioles caseros de verdura y ricota con salsa tuco', 'Ravioles con Tuco', 2100.00),
(8, 2, 'Pechuga de pollo a la grilla con vegetales salteados', 'Pollo a la Grilla', 2800.00),
(9, 2, 'Ensalada César con pollo, lechuga romana, croutons y aderezo', 'Ensalada César', 2400.00),

-- Postres
(10, 3, 'Flan casero con opción de dulce de leche o crema', 'Flan Mixto', 850.00),
(11, 3, 'Bocha de helado de crema americana con salsa de chocolate', 'Copa Helada', 900.00),
(12, 3, 'Mousse de chocolate artesanal con hilos de chocolate amargo', 'Mousse de Chocolate', 1100.00),
(13, 3, 'Tradicional postre vigilante con queso fresco y dulce de batata', 'Queso y Dulce', 950.00),

-- Bebidas
(14, 4, 'Agua mineral sin gas 500ml', 'Agua Mineral', 500.00),
(15, 4, 'Cerveza artesanal tirada de la casa 500ml', 'Cerveza Pinta', 1200.00),
(16, 4, 'Gaseosa línea Coca-Cola original de 354ml', 'Gaseosa Común', 650.00),
(17, 4, 'Copa de vino tinto Malbec de la casa', 'Copa de Vino Malbec', 1400.00);

INSERT IGNORE INTO Servicios (servicio_id, nombre) VALUES 
(1, 'Almuerzo Ejecutivo'),
(2, 'Cena a la Carta'),
(3, 'Evento Privado');

INSERT IGNORE INTO Reservas (reserva_id, fecha, email, nombre, apellido, DNI, servicio_ID, telefono, cantidad_personas, estado) VALUES 
-- Reservas Históricas (Finalizadas, habilitadas para tener reseñas)
(1, '2026-05-20', 'test@gmail.com', 'Kevin', 'La Rocca', '44123456', 2, '1123456789', 4, 'finalizada'),
(2, '2026-05-28', 'carlos.rodriguez@gmail.com', 'Carlos', 'Rodríguez', '32456789', 1, '1133445566', 2, 'finalizada'),
(3, '2026-06-02', 'ana.martinez@yahoo.com', 'Ana', 'Martínez', '39123852', 2, '1166778899', 3, 'finalizada'),

-- Reservas Pendientes / Activas (Futuras)
(4, '2026-06-15', 'juan.perez@gmail.com', 'Juan', 'Pérez', '35123456', 1, '1198765432', 2, 'reservada'),
(5, '2026-06-20', 'maria.gomez@hotmail.com', 'María', 'Gomez', '38987654', 3, '1155443322', 10, 'reservada'),
(6, '2026-06-22', 'coordinacion@empresa.com', 'Esteban', 'Quito', '28456123', 3, '1122334455', 15, 'reservada'),

-- Reservas Canceladas
(7, '2026-06-01', 'cancelado@test.com', 'Pedro', 'Mármol', '20123999', 2, '1100001111', 2, 'cancelada');

INSERT IGNORE INTO Resenas (resena_id, reserva_id, puntuacion_ambiente, puntuacion_servicio, puntuacion_comida, comentario) VALUES 
(1, 1, 4, 5, 4, 'Muy buena atención por parte del personal y los platos llegaron a tiempo. Recomendable.'),
(2, 2, 5, 4, 5, 'El ambiente es muy agradable y tranquilo para almuerzos de trabajo. Excelente calidad en los ingredientes.'),
(3, 3, 3, 4, 4, 'La comida estuvo muy bien lograda, aunque la música del salón estaba un poco alta. Volvería.');

INSERT IGNORE INTO Servicios_reserva (servicios_reserva_id, reserva_id, servicio_id) VALUES 
(1, 1, 2),
(2, 2, 1),
(3, 3, 2),
(4, 4, 1),
(5, 5, 3),
(6, 6, 3),
(7, 7, 2);

INSERT IGNORE INTO Mesas (mesa_id, estado, cantidad_personas) VALUES 
(1, 'ocupada', 4),
(2, 'desocupada', 2),
(3, 'desocupada', 6),
(4, 'desocupada', 2),
(5, 'ocupada', 8),
(6, 'desocupada', 4),
(7, 'desocupada', 12),
(8, 'ocupada', 2);