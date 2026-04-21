import sqlite3
import os
# Asegúrate de que el archivo se llame Mensajes.py y la clase Mensaje
from modelos.Mensajes import Mensaje

DB_PATH_MENSAJES = os.getenv("DB_PATH")

def guardar_mensaje(consulta: str, mensaje: Mensaje) -> bool:
    try:
        with sqlite3.connect(DB_PATH_MENSAJES) as conn:
            cursor = conn.cursor()
            # Aquí 'mensaje' sí existe porque es un parámetro de esta función
            valores = (
                mensaje.id_animalLover_emisor, 
                mensaje.id_animalLover_receptor, 
                mensaje.id_trabajo, 
                mensaje.contenido, 
                mensaje.fecha_mensaje
            )
            cursor.execute(consulta, valores)
            conn.commit()
        return True
    except Exception as e:
        print(f"Error en guardar_mensaje: {e}")
        return False

def buscar_mensajes(consulta: str, id_animalLover: int, id_trabajo: int) -> tuple[list[Mensaje], bool]:
    try:
        with sqlite3.connect(DB_PATH_MENSAJES) as conn:
            cursor = conn.cursor()
            cursor.execute(consulta, (id_animalLover, id_trabajo))
            rows = cursor.fetchall()
            
            listado_mensajes = []
            for row in rows:
                # LINEA 41: Usamos la Clase 'Mensaje' (Mayúscula) para crear el objeto
                nuevo_mensaje = Mensaje(*row) 
                listado_mensajes.append(nuevo_mensaje)
                
        return listado_mensajes, True
    except Exception as e:
        print(f"Error en buscar_mensajes: {e}")
        return [], False
def actualizar_mensaje(consulta: str, id_mensaje: int, contenido: str) -> bool:
    """
    Actualiza el contenido de un mensaje existente.
    """
    try:
        with sqlite3.connect(DB_PATH_MENSAJES) as conn:
            cursor = conn.cursor()
            cursor.execute(consulta, (contenido, id_mensaje))
            conn.commit()
            
        print(f"Mensaje actualizado correctamente: {consulta}")
        return True
    except Exception as e:
        print(f"Error al ejecutar la actualización: {e}")
        return False

def eliminar_mensaje(consulta: str, id_mensaje: int) -> bool:
    """
    Elimina un mensaje de la base de datos por su ID.
    """
    try:
        with sqlite3.connect(DB_PATH_MENSAJES) as conn:
            cursor = conn.cursor()
            cursor.execute(consulta, (id_mensaje,))
            conn.commit()
            
        print(f"Mensaje eliminado correctamente: {consulta}")
        return True
    except Exception as e:
        print(f"Error al ejecutar la eliminación: {e}")
        return False