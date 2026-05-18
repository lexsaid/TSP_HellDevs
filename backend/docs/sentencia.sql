-- 1. Tabla principal sin dependencias
CREATE TABLE animalLover (
	id_animalLover	INTEGER  PRIMARY KEY AUTOINCREMENT,
	nombre	TEXT NOT NULL,
	apellido	TEXT NOT NULL,
	email	TEXT NOT NULL UNIQUE,
	telefono	TEXT NOT NULL UNIQUE,
	contraseña	TEXT NOT NULL,
	token	TEXT
);

-- 2. Tablas que dependen directamente de AnimalLover
CREATE TABLE animal (
    id_animal INTEGER PRIMARY KEY AUTOINCREMENT,
    id_animalLover INTEGER NOT NULL,
    nombre TEXT NOT NULL,
    direccion TEXT NOT NULL,
    tamanio TEXT NOT NULL,
    color TEXT NOT NULL,
    discapacidad TEXT NOT NULL,
    tipo_animal TEXT NOT NULL,
    edad INTEGER NOT NULL,
    detalles_adicionales TEXT NOT NULL,
    FOREIGN KEY (id_animalLover) REFERENCES AnimalLover(id_animalLover)
);

CREATE TABLE albergue (
    id_albergue INTEGER PRIMARY KEY AUTOINCREMENT,
    id_animalLover INTEGER NOT NULL,
    nombre TEXT NOT NULL,
    ubicacion TEXT NOT NULL,
    capacidad INTEGER NOT NULL,
    preferencia TEXT NOT NULL, -- Valores esperados: "Perros", "Gatos"
    costo_diario INTEGER NOT NULL,
    pre_requisitos TEXT NOT NULL,
    FOREIGN KEY (id_animalLover) REFERENCES AnimalLover(id_animalLover)
);

CREATE TABLE trabajo (
	id_trabajo	INTEGER  PRIMARY KEY AUTOINCREMENT,
	nombre	TEXT NOT NULL,
	ubicacion	TEXT NOT NULL,
	fecha_publicacion	TEXT NOT NULL,
	monto	REAL NOT NULL,
	descripcion	TEXT NOT NULL,
	id_animalLover_publicador	INTEGER NOT NULL,
	tipo_trabajo	TEXT NOT NULL,
	FOREIGN KEY(id_animalLover_publicador) REFERENCES animalLover(id_animalLover)
);

-- 3. Tablas que dependen de Animal, Albergue y Trabajo
CREATE TABLE animalPerdido (
    id_animalPerdido INTEGER PRIMARY KEY,
    id_animal INTEGER NOT NULL,
    recompensa TEXT NOT NULL,
    estado TEXT NOT NULL DEFAULT 'Activo',
    FOREIGN KEY (id_animal) REFERENCES animal(id_animal)
);

CREATE TABLE animalCalle (
    id_animalCalle INTEGER PRIMARY KEY,
    id_animal INTEGER NOT NULL,
    vacunas TEXT NOT NULL,
    estado TEXT NOT NULL DEFAULT 'Activo',
    FOREIGN KEY (id_animal) REFERENCES animal(id_animal)
);

CREATE TABLE imagen_animal (
    id_imagen INTEGER PRIMARY KEY,
    id_animal INTEGER NOT NULL,
    imagen BLOB NOT NULL,
    fecha_carga TEXT NOT NULL,
    FOREIGN KEY (id_animal) REFERENCES animal(id_animal)
);

CREATE TABLE imagen_albergue (
    id_imagen INTEGER PRIMARY KEY,
    id_albergue INTEGER NOT NULL,
    imagen BLOB NOT NULL,
    fecha_carga TEXT NOT NULL,
    FOREIGN KEY (id_albergue) REFERENCES albergue(id_albergue)
);

CREATE TABLE imagen (
	id_imagen	INTEGER  PRIMARY KEY AUTOINCREMENT,
	id_trabajo	INTEGER NOT NULL,
	imagen	BLOB NOT NULL,
	FOREIGN KEY(id_trabajo) REFERENCES trabajo(id_trabajo)
);

-- 4. Tablas intermedias/transaccionales complejas (dependen de múltiples tablas)
CREATE TABLE trabajo_aceptado(
	id_trabajo	INTEGER NOT NULL,
	id_animalLover_trabajador	INTEGER NOT NULL,
	fecha_aceptacion	TEXT NOT NULL,
	estado_trabajo TEXT NOT NULL CHECK(estado_trabajo IN ("Pendiente", "Terminado", "Cancelado")),
	FOREIGN KEY(id_trabajo) REFERENCES trabajo(id_trabajo),
	FOREIGN KEY(id_animalLover_trabajador) REFERENCES animalLover(id_animalLover),
	PRIMARY KEY(id_trabajo, id_animalLover_trabajador)
);

CREATE TABLE mensajes (
	id_mensaje	INTEGER  PRIMARY KEY AUTOINCREMENT,
	id_animalLover_emisor	INTEGER NOT NULL,
	id_animalLover_receptor	INTEGER NOT NULL,
	id_trabajo	INTEGER NOT NULL,
	contenido	TEXT NOT NULL,
	fecha_mensaje	TEXT NOT NULL,
	
	FOREIGN KEY(id_animalLover_emisor) REFERENCES animalLover(id_animalLover),
	FOREIGN KEY(id_animalLover_receptor) REFERENCES animalLover(id_animalLover),
	FOREIGN KEY(id_trabajo) REFERENCES trabajo(id_trabajo)
);