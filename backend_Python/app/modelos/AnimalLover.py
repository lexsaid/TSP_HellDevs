class AnimalLover:
    def __init__(
        self,
        id_usuario: int,
        nombre: str,
        apellido: str,
        email: str,
        telefono: str,
        contrasena: str
    ):
        self.id_animal_lover = id_usuario
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.telefono = telefono
        self.contrasena = contrasena

    def to_dict(self):
        return {
            "id_usuario": self.id_animal_lover,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "email": self.email,
            "telefono": self.telefono,
            "contraseña": self.contrasena
        }