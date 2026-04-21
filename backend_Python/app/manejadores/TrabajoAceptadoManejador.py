from modelos.trabajosaceptados import TrabajoAceptado
from dto.listadotrabajosaceptados import ListaTrabajosAceptados

from repositorios.trabajoaceptadoSQLiterepo import (
    guardar_trabajo_aceptado,
    buscar_trabajos_por_usuario,
    actualizar_trabajo_aceptado,
    eliminar_trabajo_aceptado
)

def aceptar_trabajo(trabajo: TrabajoAceptado):
    consulta = """
        INSERT INTO trabajo_aceptado
        (id_trabajo, id_animalLover_trabajador, fecha_aceptacion, estado_trabajo)
        VALUES (?, ?, ?, ?)
    """
    return guardar_trabajo_aceptado(consulta, trabajo)

def obtener_lista_trabajos_aceptados(id_animalLover):
    consulta = "SELECT * FROM trabajo_aceptado WHERE id_animalLover_trabajador = ?"
    return buscar_trabajos_por_usuario(consulta, id_animalLover)

def actualizar_trabajo_aceptado_handler(trabajo: TrabajoAceptado):
    consulta = """
        UPDATE trabajo_aceptado
        SET id_trabajo = ?, id_animalLover_trabajador = ?,
            fecha_aceptacion = ?, estado_trabajo = ?
        WHERE id_trabajo = ? AND id_animalLover_trabajador = ?
    """
    return actualizar_trabajo_aceptado(consulta, trabajo)

def eliminar_trabajo_aceptado_handler(trabajo: TrabajoAceptado):
    consulta = """
        DELETE FROM trabajo_aceptado
        WHERE id_trabajo = ? AND id_animalLover_trabajador = ?
    """
    return eliminar_trabajo_aceptado(consulta, trabajo)

