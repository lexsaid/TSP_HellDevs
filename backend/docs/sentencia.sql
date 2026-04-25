CREATE TABLE animalLover (
	id_animalLover	INTEGER  PRIMARY KEY AUTOINCREMENT,
	nombre	TEXT NOT NULL,
	apellido	TEXT NOT NULL,
	email	TEXT NOT NULL,
	telefono	TEXT NOT NULL UNIQUE,
	contraseña	TEXT NOT NULL,
	token	TEXT
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

CREATE TABLE trabajo_aceptado(
	id_trabajo	INTEGER NOT NULL,
	id_animalLover_trabajador	INTEGER NOT NULL,
	fecha_aceptacion	TEXT NOT NULL,
	estado_trabajo TEXT NOT NULL CHECK(estado_trabajo IN ("Pendiente", "Terminado", "Cancelado")),
	FOREIGN KEY(id_trabajo) REFERENCES trabajo(id_trabajo),
	FOREIGN KEY(id_animalLover_trabajador) REFERENCES animalLover(id_animalLover),
	PRIMARY KEY(id_trabajo, id_animalLover_trabajador)
);

CREATE TABLE imagen (
	id_imagen	INTEGER  PRIMARY KEY AUTOINCREMENT,
	id_trabajo	INTEGER NOT NULL,
	imagen	BLOB NOT NULL,
	FOREIGN KEY(id_trabajo) REFERENCES trabajo(id_trabajo)
);