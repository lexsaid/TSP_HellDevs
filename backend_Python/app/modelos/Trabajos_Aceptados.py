class TrabajoAceptado:
    def __init__(self, id_trabajo, id_usuario, fecha_aceptacion, estado_trabajo):
        self.id_trabajo = id_trabajo
        self.id_usuario = id_usuario
        self.fecha_aceptacion = fecha_aceptacion
        self.estado_trabajo = estado_trabajo

    def to_dict(self):
        return {
            "id_trabajo": self.id_trabajo,
            "id_usuario": self.id_usuario,
            "fecha_aceptacion": self.fecha_aceptacion,
            "estado_trabajo": self.estado_trabajo
        }