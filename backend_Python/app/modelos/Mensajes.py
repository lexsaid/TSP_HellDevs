class Mensaje:
    def __init__(
        self,
        id_mensaje,
        id_animalLover_emisor,
        id_animalLover_receptor,
        id_trabajo,
        contenido,
        fecha_mensaje
    ):
        self.id_mensaje = id_mensaje
        self.id_animalLover_emisor = id_animalLover_emisor
        self.id_animalLover_receptor = id_animalLover_receptor
        self.id_trabajo = id_trabajo
        self.contenido = contenido
        self.fecha_mensaje = fecha_mensaje

    def to_dict(self):
        return {
            "id_mensaje": self.id_mensaje,
            "id_animalLover_emisor": self.id_animalLover_emisor,
            "id_animalLover_receptor": self.id_animalLover_receptor,
            "id_trabajo": self.id_trabajo,
            "contenido": self.contenido,
            "fecha_mensaje": self.fecha_mensaje
        }