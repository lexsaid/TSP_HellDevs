class Imagen:
    def __init__(self, id_imagen, id_trabajo, imagen):
        self.id_imagen = id_imagen
        self.id_trabajo = id_trabajo
        self.imagen = imagen  # bytes (BLOB)

    def to_dict(self):
        return {
            "id_imagen": self.id_imagen,
            "id_trabajo": self.id_trabajo,
            "imagen": self.imagen
        }