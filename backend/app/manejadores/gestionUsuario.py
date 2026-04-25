from repositorios import usuarioRepo
from modelos.modelos import AnimalLover

def guardarUsuario(usuario: AnimalLover) -> bool:
    consulta = "INSERT INTO animalLover (nombre, apellido, email, telefono, contraseña) VALUES (?, ?, ?, ?, ?)"
    return usuarioRepo.guardarUsuario(consulta, usuario)

def buscarUsuario(idUsuario: int) -> tuple[AnimalLover, bool]:
    consulta = "SELECT * FROM animalLover WHERE id_animalLover = ?"
    return usuarioRepo.buscarIdUsuario(consulta, idUsuario)

def actualizarUsuario(usuario: AnimalLover) -> bool:
    consulta = "UPDATE animalLover SET nombre = ?, apellido = ?, email = ?, telefono = ?, contraseña = ? WHERE id_animalLover = ?"
    return usuarioRepo.actualizarUsuario(consulta, usuario)

def eliminarUsuario(idUsuario: int) -> bool:
    consulta = "DELETE FROM animalLover WHERE id_animalLover = ?"
    return usuarioRepo.eliminarUsuario(consulta, idUsuario)
