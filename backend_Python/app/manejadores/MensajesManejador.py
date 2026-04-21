from modelos.Mensajes import Mensaje
from modelos.AnimalLover import AnimalLover

from dto.ListadoMensajes import ListadoMensajes
from dto.ListadoMensajesFinal import ListadoMensajesFinal
from dto.MensajeFinal import MensajeFinal
from dto.MensajesRemitente import MensajesRemitente

from repositorios.mensajesSQLiterepo import (
    guardar_mensaje,
    buscar_mensajes,
    actualizar_mensaje,
    eliminar_mensaje
)

from repositorios.animalloversSQLiterepo import buscar_por_id

def guardar_mensaje_handler(mensaje: Mensaje):
    consulta = """
        INSERT INTO mensajes
        (id_animalLover_emisor, id_animalLover_receptor, id_trabajo, contenido, fecha_mensaje)
        VALUES (?, ?, ?, ?, ?)
    """
    return guardar_mensaje(consulta, mensaje)

def obtener_lista_mensajes(remitente: MensajesRemitente):
    etapa1, ok = _obtener_mensajes_remitente(
        remitente.id_animalLover,
        remitente.id_trabajo
    )

    if not ok:
        return ListadoMensajesFinal([]), False

    return _agrupar_datos_mensaje(etapa1), True

def _obtener_mensajes_remitente(id_animalLover, id_trabajo):
    consulta = """
        SELECT * FROM mensajes
        WHERE id_animalLover_emisor = ? AND id_trabajo = ?
    """
    return buscar_mensajes(consulta, id_animalLover, id_trabajo)

def _agrupar_datos_mensaje(listado: ListadoMensajes):
    lista_final = ListadoMensajesFinal([])

    consulta_usuario = """
        SELECT id_animalLover, nombre, apellido, email, telefono, contraseña, token
        FROM animalLover
        WHERE id_animalLover = ?
    """

    for msg in listado.mensajes:
        remitente, _ = buscar_por_id(consulta_usuario, msg.id_usuario_envia)
        receptor, _ = buscar_por_id(consulta_usuario, msg.id_usuario_recibe)

        mensaje_final = MensajeFinal(
            id_mensaje=msg.id_mensaje,
            remitente=f"{remitente.nombre} {remitente.apellido}",
            id_remitente=msg.id_usuario_envia,
            receptor=f"{receptor.nombre} {receptor.apellido}",
            id_receptor=msg.id_usuario_recibe,
            id_trabajo=msg.id_trabajo,
            contenido=msg.contenido,
            fecha_mensaje=msg.fecha_mensaje
        )

        lista_final.mensajes.append(mensaje_final)

    return lista_final

def actualizar_mensaje_handler(id_mensaje, contenido):
    consulta = "UPDATE mensajes SET contenido = ? WHERE id_mensaje = ?"
    return actualizar_mensaje(consulta, id_mensaje, contenido)

def eliminar_mensaje_handler(id_mensaje):
    consulta = "DELETE FROM mensajes WHERE id_mensaje = ?"
    return eliminar_mensaje(consulta, id_mensaje)