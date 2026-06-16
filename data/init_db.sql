SET NAMES 'utf8mb4';

-- CREACIÓN DE BASE DE DATOS
CREATE DATABASE IF NOT EXISTS gastronomia_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE gastronomia_db;

--  codificacion
ALTER DATABASE `gastronomia_db` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- TABLA: Usuarios
CREATE TABLE IF NOT EXISTS Usuarios (
    usuario_id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    nombre_usuario VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    contrasena VARCHAR(255) NOT NULL,
    rol VARCHAR(30) NOT NULL CHECK (rol IN ('cliente', 'admin'))
);

-- TABLA: Categorias
CREATE TABLE IF NOT EXISTS Categorias (
    categorias_id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL UNIQUE
);

-- TABLA: Productos
CREATE TABLE IF NOT EXISTS Productos (
    producto_id INT PRIMARY KEY AUTO_INCREMENT,
    categorias_id INT NOT NULL,
    descripcion VARCHAR(300),
    nombre VARCHAR(100) NOT NULL,
    precio DECIMAL(10, 2) NOT NULL CHECK (precio >= 0),
    imagen_url VARCHAR(500) NULL,
    FOREIGN KEY (categorias_id) REFERENCES Categorias(categorias_id) ON DELETE RESTRICT
);

-- TABLA: Servicios
CREATE TABLE IF NOT EXISTS Servicios (
    servicio_id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    estado VARCHAR(20) NOT NULL DEFAULT 'habilitado' CHECK (estado IN ('habilitado', 'deshabilitado'))
);

-- TABLA: Reservas
CREATE TABLE IF NOT EXISTS Reservas (
    reserva_id INT PRIMARY KEY AUTO_INCREMENT,
    fecha DATETIME NOT NULL,
    email VARCHAR(100) NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    DNI VARCHAR(12) NOT NULL,
    telefono VARCHAR(20) NOT NULL,
    cantidad_personas INT NOT NULL CHECK (cantidad_personas > 0),
    comentario VARCHAR(300),
    estado VARCHAR(30) NOT NULL DEFAULT 'reservada' CHECK (estado IN ('reservada', 'cancelada', 'finalizada'))
    );

-- TABLA: Resenas
CREATE TABLE IF NOT EXISTS Resenas (
    resena_id INT PRIMARY KEY AUTO_INCREMENT,
    reserva_id INT NOT NULL UNIQUE,
    puntuacion_ambiente INT NOT NULL CHECK (puntuacion_ambiente BETWEEN 1 AND 5),
    puntuacion_servicio INT NOT NULL CHECK (puntuacion_servicio BETWEEN 1 AND 5),
    puntuacion_comida INT NOT NULL CHECK (puntuacion_comida BETWEEN 1 AND 5),
    comentario TEXT NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado VARCHAR(20) NOT NULL DEFAULT 'habilitada' CHECK (estado IN ('habilitada', 'deshabilitada')),
    FOREIGN KEY (reserva_id) REFERENCES Reservas(reserva_id) ON DELETE CASCADE
);

-- TABLA: Servicios_reserva
CREATE TABLE IF NOT EXISTS Servicios_reserva (
    servicios_reserva_id INT PRIMARY KEY AUTO_INCREMENT,
    reserva_id INT NOT NULL,
    servicio_id INT NOT NULL,
    FOREIGN KEY (reserva_id) REFERENCES Reservas(reserva_id) ON DELETE CASCADE,
    FOREIGN KEY (servicio_id) REFERENCES Servicios(servicio_id) ON DELETE RESTRICT
);

-- TABLA: Mesas
CREATE TABLE IF NOT EXISTS Mesas (
    mesa_id INT PRIMARY KEY AUTO_INCREMENT,
    estado VARCHAR(20) NOT NULL CHECK (estado IN ('ocupada', 'desocupada')),
    cantidad_mesas INT NOT NULL CHECK (cantidad_mesas > 0)
);


-- -------------------------------- DATOS EJEMPLO PARA BASE DE DATOS --------------------------------

-- Usuarios
INSERT IGNORE INTO Usuarios (usuario_id, nombre, apellido, nombre_usuario, email, contrasena, rol) VALUES 
(1, 'El', 'Supremo', 'El_Supremo', 'el_Supremon@test.com', 'hashed_password_777', 'admin'),
(2, 'Kevin', 'La Rocca', 'kevin_dev', 'kevin@test.com', 'hashed_password_123', 'admin'),
(3, 'Carla', 'Kim', 'carla_admin', 'carla@test.com', 'hashed_password_456', 'admin'),
(4, 'Ulfric', 'Stormcloak', 'ulfric_windhelm', 'ulfric@skyrim.com', 'hashed_password_456', 'cliente'),
(5, 'Lydia', 'Housecarl', 'lydia_guard', 'lydia@skyrim.com', 'hashed_password_789', 'cliente'),
(6, 'Balgruuf', 'The Greater', 'jarl_balgruuf', 'balgruuf@skyrim.com', 'hashed_password_101', 'cliente'),
(7, 'Delphine', 'Blade', 'delphine_blades', 'delphine@skyrim.com', 'hashed_password_202', 'cliente');

-- Categorias
INSERT IGNORE INTO Categorias (categorias_id, nombre) VALUES 
(1, 'Entradas'),
(2, 'Platos Principales'),
(3, 'Postres'),
(4, 'Bebidas'),
(5, 'Especialidades Nórdicas');

INSERT IGNORE INTO Productos (producto_id, categorias_id, descripcion, nombre, precio, imagen_url) VALUES 
-- Entradas
(1, 1, 'Empanada de carne cortada a cuchillo, frita', 'Empanada de Carne', 450.00, NULL),
(2, 1, 'Provoleta tradicional a la chapa con orégano y oliva', 'Provoleta Clásica', 1800.00, NULL),
(3, 1, 'Porción de papas fritas bastón crujientes', 'Papas Fritas Medianas', 1100.00, "https://uepxnfxlzaljovgxobqd.supabase.co/storage/v1/object/public/productos/papas.jpg"),
(4, 1, 'Bastones de muzzarella rebozados acompañados de salsa pomodoro', 'Bastones de Muzzarella', 1500.00, NULL),

-- Platos Principales
(5, 2, 'Milanesa de ternera acompañada de papas fritas', 'Milanesa Clásica', 1250.00, NULL),
(6, 2, 'Bife de chorizo de 400g con guarnición a elección', 'Bife de Chorizo', 4200.00, NULL),
(7, 2, 'Ravioles caseros de verdura y ricota con salsa tuco', 'Ravioles con Tuco', 2100.00, NULL),
(8, 2, 'Pechuga de pollo a la grilla con vegetales salteados', 'Pollo a la Grilla', 2800.00, NULL),
(9, 2, 'Ensalada César con pollo, lechuga romana, croutons y aderezo', 'Ensalada César', 2400.00, NULL),

-- Postres
(10, 3, 'Flan casero con opción de dulce de leche o crema', 'Flan Mixto', 850.00, NULL),
(11, 3, 'Bocha de helado de crema americana con salsa de chocolate', 'Copa Helada', 900.00, NULL),
(12, 3, 'Mousse de chocolate artesanal con hilos de chocolate amargo', 'Mousse de Chocolate', 1100.00, NULL),
(13, 3, 'Tradicional postre vigilante con queso fresco y dulce de batata', 'Queso y Dulce', 950.00, NULL),

-- Bebidas
(14, 4, 'Agua mineral sin gas 500ml', 'Agua Mineral', 500.00, NULL),
(15, 4, 'Cerveza artesanal tirada de la casa 500ml', 'Cerveza Pinta', 1200.00, NULL),
(16, 4, 'Gaseosa línea Coca-Cola original de 354ml', 'Gaseosa Común', 650.00, NULL),
(17, 4, 'Copa de vino tinto Malbec de la casa', 'Copa de Vino Malbec', 1400.00, NULL),

-- Especialidades Nórdicas
(18, 5, 'Costillas asadas con especias de Skyrim', 'Costillas de Carrera Blanca', 3200.00, NULL),
(19, 5, 'Bebida dulce inspirada en la famosa hidromiel', 'Hidromiel Honningbrew', 950.00, NULL),
(20, 5, 'Tarta de manzana tradicional', 'Tarta de Soledad', 1400.00, NULL),
(21, 5, 'Estofado caliente ideal para aventureros', 'Estofado del Sangre de Dragón', 2800.00, NULL);

-- Servicios
INSERT IGNORE INTO Servicios (servicio_id, nombre) VALUES 
(1, 'Estacionamiento'),
(2, 'Terraza'),
(3, 'Evento Privado'),
(4, 'Asiento para bebe');

-- Reservas
INSERT IGNORE INTO Reservas (reserva_id, fecha, email, nombre, apellido, DNI, telefono, cantidad_personas, comentario, estado) VALUES 

-- Reservas Históricas (Finalizadas, habilitadas para tener reseñas)
(1, '2026-05-10', 'test@gmail.com', 'Kevin', 'La Rocca', '44123456', '1123456789', 4, 'comentario1', 'finalizada'),
(2, '2026-05-11', 'carlos.rodriguez@gmail.com', 'Carlos', 'Rodríguez', '32456789', '1133445566', 2, 'comentario2', 'finalizada'),
(3, '2026-06-12', 'ana.martinez@yahoo.com', 'Ana', 'Martínez', '39123852', '1166778899', 3, 'comentario3', 'finalizada'),
(4, '2026-06-13', 'juan.perez@gmail.com', 'Juan', 'Pérez', '35123456', '1198765432', 2, NULL, 'finalizada'),
(5, '2026-06-14', 'maria.gomez@hotmail.com', 'María', 'Gomez', '38987654', '1155443322', 4, NULL, 'finalizada'),
(6, '2026-06-15', 'lydia@skyrim.com', 'Lydia', 'Housecarl', '44222222', '2222222222', 2, NULL, 'finalizada'),
(7, '2026-05-16', 'test@gmail.com', 'Kevin', 'La Rocca', '44123456', '1123456789', 4, NULL, 'finalizada'),
(8, '2026-05-17', 'carlos.rodriguez@gmail.com', 'Carlos', 'Rodríguez', '32456789', '1133445566', 2, NULL, 'finalizada'),
(9, '2026-06-17', 'ana.martinez@yahoo.com', 'Ana', 'Martínez', '39123852', '1166778899', 3, NULL, 'finalizada'),
(10, '2026-06-18', 'juan.perez@gmail.com', 'Juan', 'Pérez', '35123456', '1198765432', 2, NULL,'finalizada'),
(11, '2026-06-19', 'maria.gomez@hotmail.com', 'María', 'Gomez', '38987654', '1155443322', 4, NULL, 'finalizada'),
(12, '2026-06-20', 'lydia@skyrim.com', 'Lydia', 'Housecarl', '44222222', '2222222222', 2, NULL,'finalizada'),

-- Reservas Pendientes / Activas (Futuras)
(13, '2026-07-15', 'juan.perez@gmail.com', 'Juan', 'Pérez', '35123456', '1198765432', 2, NULL, 'reservada'),
(14, '2026-07-20', 'maria.gomez@hotmail.com', 'María', 'Gomez', '38987654', '1155443322', 10, NULL, 'reservada'),
(15, '2026-07-22', 'coordinacion@empresa.com', 'Esteban', 'Quito', '28456123', '1122334455', 15, NULL,'reservada'),
(16, '2026-07-17', 'juan.perez@gmail.com', 'Juan', 'Pérez', '35123456', '1198765432', 2, NULL, 'reservada'),
(17, '2026-07-23', 'maria.gomez@hotmail.com', 'María', 'Gomez', '38987654', '1155443322', 10, NULL, 'reservada'),
(18, '2026-07-29', 'coordinacion@empresa.com', 'Esteban', 'Quito', '28456123', '1122334455', 15, NULL, 'reservada'),

-- Reservas Canceladas
(19, '2026-06-01', 'cancelado@test.com', 'Pedro', 'Mármol', '20123999', '1100001111', 2, NULL,'cancelada'),
(20, '2026-06-02', 'delphine@skyrim.com', 'Delphine', 'Blade', '44444444', '4444444444', 3, NULL, 'cancelada');

-- Resenas
INSERT IGNORE INTO Resenas (resena_id, reserva_id, puntuacion_ambiente, puntuacion_servicio, puntuacion_comida, comentario) VALUES 
(1, 1, 4, 5, 4, 'Muy buena atención por parte del personal y los platos llegaron a tiempo. Recomendable.'),
(2, 2, 5, 4, 5, 'El ambiente es muy agradable y tranquilo para almuerzos de trabajo. Excelente calidad en los ingredientes.'),
(3, 3, 3, 4, 4, 'La comida estuvo muy bien lograda, aunque la música del salón estaba un poco alta. Volvería.'),
(4, 4, 1, 1, 1, 'No lo recomiendo para nada. Me trajeron una empanada de carne como bebida.'),
(5, 5, 5, 5, 5, 'Las empanadas de carne y las pastas caseras son exquisitas. Hubo una pequeña demora con las bebidas, pero el sabor de la comida lo compensó por completo.'),
(6, 6, 5, 4, 5, 'Casi tan acogedor como Carrera Blanca.'),
(7, 7, 4, 5, 4, 'Recomendable.'),
(8, 8, 5, 4, 5, 'Excelente calidad en los ingredientes.'),
(9, 9, 3, 4, 4, 'La comida estuvo muy bien lograda. Volvería.'),
(10, 10, 5, 5, 5, 'Una experiencia gastronómica impecable. El bife de chorizo estaba en el punto exacto solicitado y la atención fue de primer nivel.'),
(11, 11, 4, 3, 5, 'Hubo una pequeña demora con las bebidas, pero el sabor de la comida lo compensó por completo.'),
(12, 12, 5, 4, 5, 'El lugar estaba impecable, parecia que estaba en el palacio de Soldad.');

-- Servicios_reserva
INSERT IGNORE INTO Servicios_reserva (servicios_reserva_id, reserva_id, servicio_id) VALUES 
(1, 1, 2),
(2, 2, 1),
(3, 3, 2),
(4, 4, 1),
(5, 5, 3),
(6, 6, 3),
(7, 7, 2),
(8, 8, 2),
(9, 9, 1),
(10, 10, 4),
(11, 10, 3),
(12, 12, 1),
(13, 13, 2),
(14, 14, 1),
(15, 15, 3),
(16, 16, 3),
(17, 17, 2),
(18, 18, 2),
(19, 19, 1),
(20, 19, 2),
(21, 19, 3),
(22, 19, 4);

-- Mesas
INSERT IGNORE INTO Mesas (mesa_id, estado, cantidad_mesas) VALUES 
(1, 'ocupada', 27),
(2, 'desocupada', 43);