import os
import sqlite3

from modelos.Imagen import Imagen
from dto.listadoImagenes import ListadoImagenes

DB_PATH = os.getenv("DB_PATH")

def guardar_imagen(consulta):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute(consulta)
        conn.commit()
        conn.close()

        print("Imagen guardada correctamente:", consulta)
        return True

    except Exception as e:
        print("Error al ejecutar la consulta en imagen:", e)
        return False
    
def buscar_imagenes(consulta):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute(consulta)
        filas = cursor.fetchall()
        conn.close()

        imagenes = []

        for fila in filas:
            # fila = (id_imagen, id_trabajo, imagen_blob)
            imagen = Imagen(
                fila[0],  # id_imagen
                fila[1],  # id_trabajo
                fila[2]   # imagen (bytes)
            )
            imagenes.append(imagen)

        print("Imagenes encontradas correctamente:", consulta)
        return ListadoImagenes(imagenes), True

    except Exception as e:
        print("Error al buscar las imagenes:", e)
        return ListadoImagenes([]), False
    
def actualizar_imagen(consulta):
    return guardar_imagen(consulta)

def eliminar_imagen(consulta):
    return guardar_imagen(consulta)