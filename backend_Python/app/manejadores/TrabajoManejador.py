from modelos.Trabajo import Trabajo
from repositorios.trabajoaceptadoSQLiterepo import (
    guardar_trabajo,
    buscar_trabajo_por_id,
    actualizar_trabajo,
    eliminar_trabajo
)

def crear_trabajo(trabajo: Trabajo):
    consulta = """
        INSERT INTO trabajo
        (nombre, ubicacion, fecha_publicacion, monto, descripcion,
         id_animalLover_publicador, tipo_trabajo, estado)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """
    return guardar_trabajo(consulta, trabajo)

def obtener_trabajo(id_trabajo):
    consulta = "SELECT * FROM trabajo WHERE id_trabajo = ?"
    return buscar_trabajo_por_id(consulta, id_trabajo)

def actualizar_trabajo_handler(trabajo: Trabajo):
    consulta = """
        UPDATE trabajo
        SET nombre = ?, ubicacion = ?, fecha_publicacion = ?, monto = ?,
            descripcion = ?, id_animalLover_publicador = ?, tipo_trabajo = ?, estado = ?
        WHERE id_trabajo = ?
    """
    return actualizar_trabajo(consulta, trabajo)

def eliminar_trabajo_handler(trabajo: Trabajo):
    consulta = "DELETE FROM trabajo WHERE id_trabajo = ?"
    return eliminar_trabajo(consulta, trabajo)