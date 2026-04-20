class ListadoImagenes:
    def __init__(self, imagenes):
        self.imagenes = imagenes

    def to_dict(self):
        return {
            "imagenes": [img.to_dict() for img in self.imagenes]
        }