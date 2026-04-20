class TrabajoAceptado:
    def __init__(
        self,
        id_trabajo,
        id_animalLover_trabajador,
        fecha_aceptacion,
        estado_trabajo
    ):
        self.id_trabajo = id_trabajo
        self.id_animalLover_trabajador = id_animalLover_trabajador
        self.fecha_aceptacion = fecha_aceptacion
        self.estado_trabajo = estado_trabajo  # Pendiente | Terminado | Cancelado

    def to_dict(self):
        return {
            "id_trabajo": self.id_trabajo,
            "id_animalLover_trabajador": self.id_animalLover_trabajador,
            "fecha_aceptacion": self.fecha_aceptacion,
            "estado_trabajo": self.estado_trabajo
        }