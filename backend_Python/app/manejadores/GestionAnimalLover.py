from modelos.AnimalLover import AnimalLover
from repositorios.animalloversSQLiterepo import (
    guardar,
    buscar_por_id,
    actualizar,
    eliminar
)

def guardar_animal_lover(animal_lover: AnimalLover):
    consulta = """
        INSERT INTO animalLover
        (nombre, apellido, email, telefono, contraseña)
        VALUES (?, ?, ?, ?, ?)
    """
    return guardar(consulta, animal_lover)

def buscar_animal_lover(animal_lover: AnimalLover):
    consulta = "SELECT * FROM animalLover WHERE id_animalLover = ?"
    return buscar_por_id(consulta, animal_lover.id_animalLover)

def actualizar_animal_lover(animal_lover: AnimalLover):
    consulta = """
        UPDATE animalLover
        SET nombre = ?, apellido = ?, email = ?, telefono = ?, contraseña = ?
        WHERE id_animalLover = ?
    """
    return actualizar(consulta, animal_lover)

def eliminar_animal_lover(animal_lover: AnimalLover):
    consulta = "DELETE FROM animalLover WHERE id_animalLover = ?"
    return eliminar(consulta, animal_lover)