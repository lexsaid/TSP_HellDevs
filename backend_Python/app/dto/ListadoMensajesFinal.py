class ListadoMensajesFinal:
    def __init__(self, mensajes=None):
        if mensajes is None:
            mensajes = []
        self.mensajes = mensajes

    def to_dict(self):
        resultado = []
        for mensaje in self.mensajes:
            resultado.append(mensaje.to_dict())

        return {
            "mensajes": resultado
        }