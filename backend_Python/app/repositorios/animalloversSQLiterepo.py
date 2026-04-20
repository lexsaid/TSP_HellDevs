import os
import sqlite3
from modelos.animallover import AnimalLover

DB_PATH = os.getenv("DB_PATH")

def guardar(consulta, animal_lover: AnimalLover):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute(
            consulta,
            (
                animal_lover.nombre,
                animal_lover.apellido,
                animal_lover.email,
                animal_lover.telefono,
                animal_lover.contrasena
            )
        )

        conn.commit()
        conn.close()

        print("AnimalLover guardado correctamente:", consulta)
        return True

    except Exception as e:
        print("Error al ejecutar la consulta en AnimalLover:", e)
        return False

def buscar_por_id(consulta, id_animalLover):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute(consulta, (id_animalLover,))
        fila = cursor.fetchone()
        conn.close()

        if fila is None:
            return None, False

        animal_lover = AnimalLover(
            fila[0],  # id_animalLover
            fila[1],  # nombre
            fila[2],  # apellido
            fila[3],  # email
            fila[4],  # telefono
            fila[5],  # contraseña
            fila[6]   # token
        )

        print("AnimalLover encontrado correctamente:", consulta)
        return animal_lover, True

    except Exception as e:
        print("Error al buscar el AnimalLover:", e)
        return None, False

def buscar_por_email(email):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        consulta = "SELECT * FROM animalLover WHERE email = ?"
        cursor.execute(consulta, (email,))
        fila = cursor.fetchone()
        conn.close()

        if fila is None:
            return None, False

        animal_lover = AnimalLover(
            fila[0],
            fila[1],
            fila[2],
            fila[3],
            fila[4],
            fila[5],
            fila[6]
        )

        return animal_lover, True

    except Exception as e:
        print("Error al buscar AnimalLover por email:", e)
        return None, False
    
def actualizar(consulta, animal_lover):
    return guardar(consulta, animal_lover)

def eliminar(consulta, animal_lover):
    return guardar(consulta, animal_lover)