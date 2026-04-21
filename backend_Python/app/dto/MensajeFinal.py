class MensajeFinal:
    def __init__(
        self,
        id_mensaje,
        remitente,
        id_remitente,
        receptor,
        id_receptor,
        id_trabajo,
        contenido,
        fecha_mensaje
    ):
        self.id_mensaje = id_mensaje
        self.remitente = remitente
        self.id_remitente = id_remitente
        self.receptor = receptor
        self.id_receptor = id_receptor
        self.id_trabajo = id_trabajo
        self.contenido = contenido
        self.fecha_mensaje = fecha_mensaje

    def to_dict(self):
        return {
            "id_mensaje": self.id_mensaje,
            "remitente": self.remitente,
            "id_remitente": self.id_remitente,
            "receptor": self.receptor,
            "id_receptor": self.id_receptor,
            "id_trabajo": self.id_trabajo,
            "contenido": self.contenido,
            "fecha_mensaje": self.fecha_mensaje
        }