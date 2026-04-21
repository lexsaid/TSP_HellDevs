import os
import sqlite3

from modelos.trabajosaceptados import TrabajoAceptado
from dto.listadotrabajosaceptados import ListaTrabajosAceptados

DB_PATH = os.getenv("DB_PATH")

def guardar_trabajo_aceptado(consulta, trabajo: TrabajoAceptado):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute(
            consulta,
            (
                trabajo.id_trabajo,
                trabajo.id_animalLover_trabajador,
                trabajo.fecha_aceptacion,
                trabajo.estado_trabajo
            )
        )

        conn.commit()
        conn.close()

        print("Trabajo aceptado guardado correctamente:", consulta)
        return True

    except Exception as e:
        print("Error al ejecutar la consulta en trabajos aceptados:", e)
        return False
    
def buscar_trabajos_por_usuario(consulta, id_animalLover):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute(consulta, (id_animalLover,))
        filas = cursor.fetchall()
        conn.close()

        trabajos_aceptados = []

        for fila in filas:
            # fila = (id_trabajo, id_animalLover_trabajador, fecha_aceptacion, estado_trabajo)
            trabajo = TrabajoAceptado(
                fila[0],  # id_trabajo
                fila[1],  # id_animalLover_trabajador
                fila[2],  # fecha_aceptacion
                fila[3]   # estado_trabajo
            )
            trabajos_aceptados.append(trabajo)

            print("Trabajo aceptado encontrado correctamente:", consulta)

        return ListaTrabajosAceptados(trabajos_aceptados), True

    except Exception as e:
        print("Error al buscar trabajos aceptados:", e)
        return ListaTrabajosAceptados([]), False
    
def actualizar_trabajo_aceptado(consulta, trabajo):
    return guardar_trabajo_aceptado(consulta, trabajo)

def eliminar_trabajo_aceptado(consulta, trabajo):
    return guardar_trabajo_aceptado(consulta, trabajo)