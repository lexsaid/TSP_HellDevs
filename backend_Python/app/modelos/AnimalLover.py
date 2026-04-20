class AnimalLover:
    def __init__(
        self,
        id_animalLover,
        nombre,
        apellido,
        email,
        telefono,
        contrasena,
        token=None
    ):
        self.id_animalLover = id_animalLover
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.telefono = telefono
        self.contrasena = contrasena
        self.token = token

    def to_dict(self):
        return {
            "id_animalLover": self.id_animalLover,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "email": self.email,
            "telefono": self.telefono,
            "contraseña": self.contrasena,
            "token": self.token
        }