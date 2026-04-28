from repositorios.database import getDbConnection
from modelos.modelos import Mensaje
import sqlite3

def guardarMensaje(consulta: str, mensaje: Mensaje) -> bool:
    try:
        conn = getDbConnection()
        cursor = conn.cursor()
        cursor.execute(consulta, (
            mensaje.idAnimalLoverEmisor, 
            mensaje.idAnimalLoverReceptor, 
            mensaje.idTrabajo, 
            mensaje.contenido, 
            mensaje.fechaMensaje
        ))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error al ejecutar la consulta en mensajes: {e}")
        return False
    finally:
        if 'conn' in locals():
            conn.close()

def buscarMensajes(consulta: str, idUsuario: int, idOtroUsuario: int, idTrabajo: int) -> tuple[list[Mensaje], bool]:
    try:
        conn = getDbConnection()
        cursor = conn.cursor()
        cursor.execute(consulta, (idTrabajo, idUsuario, idOtroUsuario, idOtroUsuario, idUsuario))
        rows = cursor.fetchall()
        
        mensajes = []
        for row in rows:
            mensaje = Mensaje(
                idMensaje=row['id_mensaje'],
                idAnimalLoverEmisor=row['id_animalLover_emisor'],
                idAnimalLoverReceptor=row['id_animalLover_receptor'],
                idTrabajo=row['id_trabajo'],
                contenido=row['contenido'],
                fechaMensaje=row['fecha_mensaje']
            )
            mensajes.append(mensaje)
            
        return mensajes, True
    except sqlite3.Error as e:
        print(f"Error al buscar el mensaje: {e}")
        return [], False
    finally:
        if 'conn' in locals():
            conn.close()

def actualizarMensaje(consulta: str, idMensaje: int, contenido: str) -> bool:
    try:
        conn = getDbConnection()
        cursor = conn.cursor()
        cursor.execute(consulta, (contenido, idMensaje))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error al actualizar la consulta en mensajes: {e}")
        return False
    finally:
        if 'conn' in locals():
            conn.close()

def eliminarMensaje(consulta: str, idMensaje: int) -> bool:
    try:
        conn = getDbConnection()
        cursor = conn.cursor()
        cursor.execute(consulta, (idMensaje,))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error al eliminar la consulta en mensajes: {e}")
        return False
    finally:
        if 'conn' in locals():
            conn.close()

def buscarMensajesPorUsuario(consulta: str, idUsuario: int) -> tuple[list[Mensaje], bool]:
    try:
        conn = getDbConnection()
        cursor = conn.cursor()
        cursor.execute(consulta, (idUsuario, idUsuario))
        rows = cursor.fetchall()
        
        mensajes = []
        for row in rows:
            mensaje = Mensaje(
                idMensaje=row['id_mensaje'],
                idAnimalLoverEmisor=row['id_animalLover_emisor'],
                idAnimalLoverReceptor=row['id_animalLover_receptor'],
                idTrabajo=row['id_trabajo'],
                contenido=row['contenido'],
                fechaMensaje=row['fecha_mensaje']
            )
            mensajes.append(mensaje)
            
        return mensajes, True
    except sqlite3.Error as e:
        print(f"Error al buscar mensajes del usuario: {e}")
        return [], False
    finally:
        if 'conn' in locals():
            conn.close()

def contarMensajesNuevos(consulta: str, idUsuario: int, ultimoIdMensaje: int) -> bool:
    try:
        conn = getDbConnection()
        cursor = conn.cursor()
        cursor.execute(consulta, (idUsuario, ultimoIdMensaje))
        row = cursor.fetchone()
        return row['total'] > 0 if row else False
    except sqlite3.Error as e:
        print(f"Error al contar mensajes nuevos: {e}")
        return False
    finally:
        if 'conn' in locals():
            conn.close()


def eliminarMensajesPorTrabajo(idTrabajo: int) -> bool:
    try:
        conn = getDbConnection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM mensajes WHERE id_trabajo = ?", (idTrabajo,))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error al eliminar mensajes por trabajo: {e}")
        return False
    finally:
        if 'conn' in locals():
            conn.close()
