CREATE TABLE Usuario (
	id_usuario	INTEGER  PRIMARY KEY AUTOINCREMENT,
	nombre	TEXT NOT NULL,
	apellido	TEXT NOT NULL,
	email	TEXT NOT NULL,
	telefono	TEXT NOT NULL UNIQUE,
	contraseña	TEXT NOT NULL
);

CREATE TABLE Mensajes (
	id_mensaje	INTEGER  PRIMARY KEY AUTOINCREMENT,
	id_usuario_envia	INTEGER NOT NULL,
	id_usuario_recibe	INTEGER NOT NULL,
	id_trabajo	INTEGER NOT NULL,
	contenido	TEXT NOT NULL,
	fecha_mensaje	TEXT NOT NULL,
	
	FOREIGN KEY(id_usuario_envia) REFERENCES Usuario(id_usuario),
	FOREIGN KEY(id_usuario_recibe) REFERENCES Usuario(id_usuario),
	FOREIGN KEY(id_trabajo) REFERENCES Trabajo(id_trabajo)
);

CREATE TABLE Trabajo (
	id_trabajo	INTEGER  PRIMARY KEY AUTOINCREMENT,
	ubicacion	TEXT NOT NULL,
	fecha_publicacion	TEXT NOT NULL,
	monto	REAL NOT NULL,
	descripcion	TEXT NOT NULL,
	id_usuario	INTEGER NOT NULL,
	tipo_trabajo	TEXT NOT NULL,
	estado	TEXT NOT NULL,
	FOREIGN KEY(id_usuario) REFERENCES Usuario(id_usuario)
);

CREATE TABLE Trabajo_aceptado(
	id_trabajo	INTEGER NOT NULL,
	id_usuario	INTEGER NOT NULL,
	fecha_aceptacion	TEXT NOT NULL,
	estado_trabajo TEXT NOT NULL CHECK("Pendiente", "Terminado", "Cancelado"),
	FOREIGN KEY(id_trabajo) REFERENCES Trabajo(id_trabajo),
	FOREIGN KEY(id_usuario) REFERENCES Usuario(id_usuario),
	PRIMARY KEY(id_trabajo, id_usuario)
);

CREATE TABLE Imagen (
	id_imagen	INTEGER  PRIMARY KEY AUTOINCREMENT,
	id_trabajo	INTEGER NOT NULL,
	imagen	BLOB NOT NULL,
	FOREIGN KEY(id_trabajo) REFERENCES Trabajo(id_trabajo)
);