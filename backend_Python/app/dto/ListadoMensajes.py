class ListadoMensajes:
    def __init__(self, mensajes):
        # mensajes: lista de objetos Mensaje
        self.mensajes = mensajes

    def to_dict(self):
        resultado = []
        for mensaje in self.mensajes:
            resultado.append(mensaje.to_dict())

        return {
            "mensajes": resultado
        }