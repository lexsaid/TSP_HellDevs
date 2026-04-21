import os
import sqlite3

from modelos.trabajo import Trabajo

DB_PATH = os.getenv("DB_PATH")

def guardar_trabajo(consulta, trabajo: Trabajo):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute(
            consulta,
            (
                trabajo.nombre,
                trabajo.ubicacion,
                trabajo.fecha_publicacion,
                trabajo.monto,
                trabajo.descripcion,
                trabajo.id_animalLover_publicador,
                trabajo.tipo_trabajo,
                trabajo.estado
            )
        )

        conn.commit()
        conn.close()

        print("Trabajo guardado correctamente:", consulta)
        return True

    except Exception as e:
        print("Error al ejecutar la consulta en trabajo:", e)
        return False
    
def buscar_trabajo_por_id(consulta, id_trabajo):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute(consulta, (id_trabajo,))
        fila = cursor.fetchone()
        conn.close()

        if fila is None:
            return None, False

        trabajo = Trabajo(
            fila[0],  # id_trabajo
            fila[1],  # nombre
            fila[2],  # ubicacion
            fila[3],  # fecha_publicacion
            fila[4],  # monto
            fila[5],  # descripcion
            fila[6],  # id_animalLover_publicador
            fila[7],  # tipo_trabajo
            fila[8]   # estado
        )

        print("Trabajo encontrado correctamente:", consulta)
        return trabajo, True

    except Exception as e:
        print("Error al buscar el trabajo:", e)
        return None, False
    
def actualizar_trabajo(consulta, trabajo):
    return guardar_trabajo(consulta, trabajo)

def eliminar_trabajo(consulta, trabajo):
    return guardar_trabajo(consulta, trabajo)