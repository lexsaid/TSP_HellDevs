class Trabajo:
    def __init__(
        self,
        id_trabajo,
        nombre,
        ubicacion,
        fecha_publicacion,
        monto,
        descripcion,
        id_animalLover_publicador,
        tipo_trabajo,
        estado
    ):
        self.id_trabajo = id_trabajo
        self.nombre = nombre
        self.ubicacion = ubicacion
        self.fecha_publicacion = fecha_publicacion
        self.monto = monto
        self.descripcion = descripcion
        self.id_animalLover_publicador = id_animalLover_publicador
        self.tipo_trabajo = tipo_trabajo
        self.estado = estado

    def to_dict(self):
        return {
            "id_trabajo": self.id_trabajo,
            "nombre": self.nombre,
            "ubicacion": self.ubicacion,
            "fecha_publicacion": self.fecha_publicacion,
            "monto": self.monto,
            "descripcion": self.descripcion,
            "id_animalLover_publicador": self.id_animalLover_publicador,
            "tipo_trabajo": self.tipo_trabajo,
            "estado": self.estado
        }