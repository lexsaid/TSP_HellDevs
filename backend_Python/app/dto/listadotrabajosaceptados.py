class ListaTrabajosAceptados:
    def __init__(self, trabajos_aceptados):
        # trabajos_aceptados: lista de objetos TrabajoAceptado
        self.trabajos_aceptados = trabajos_aceptados

    def to_dict(self):
        resultado = []
        for trabajo in self.trabajos_aceptados:
            resultado.append(trabajo.to_dict())

        return {
            "trabajos_aceptados": resultado
        }