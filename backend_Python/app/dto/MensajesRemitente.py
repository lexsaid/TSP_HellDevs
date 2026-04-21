class MensajesRemitente:
    def __init__(self, id_animalLover, id_trabajo):
        self.id_animalLover = id_animalLover
        self.id_trabajo = id_trabajo

    def to_dict(self):
        return {
            "id_animalLover": self.id_animalLover,
            "id_trabajo": self.id_trabajo
        }