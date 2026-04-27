from repositorios.database import getDbConnection
from modelos.modelos import Albergue, AlbergueDetalle, AnimalLoverDetalle
import sqlite3

def guardarAlbergue(albergue: Albergue) -> int:
    try:
        conn = getDbConnection()
        cursor = conn.cursor()
        consulta = """
            INSERT INTO albergue (id_animalLover, nombre, ubicacion, capacidad, preferencia, costo_diario, pre_requisitos)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        cursor.execute(consulta, (
            albergue.idAnimalLover,
            albergue.nombre,
            albergue.ubicacion,
            albergue.capacidad,
            albergue.preferencia,
            albergue.costoDiario,
            albergue.preRequisitos
        ))
        conn.commit()
        return cursor.lastrowid
    except sqlite3.Error as e:
        print(f"Error al ejecutar la consulta en guardarAlbergue: {e}")
        return -1
    finally:
        if 'conn' in locals():
            conn.close()

def buscarTodosAlbergues() -> tuple[list[AlbergueDetalle], bool]:
    try:
        conn = getDbConnection()
        cursor = conn.cursor()
        consulta = """
            SELECT 
                a.id_albergue, a.id_animalLover, a.nombre as albergue_nombre, a.ubicacion, a.capacidad, a.preferencia, a.costo_diario, a.pre_requisitos,
                al.nombre as dueno_nombre, al.apellido, al.telefono, al.email
            FROM albergue a
            INNER JOIN animalLover al ON a.id_animalLover = al.id_animalLover
            ORDER BY a.id_albergue DESC
        """
        cursor.execute(consulta)
        rows = cursor.fetchall()
        albergues_detalle = []
        for row in rows:
            albergue = Albergue(
                idAlbergue=row['id_albergue'],
                idAnimalLover=row['id_animalLover'],
                nombre=row['albergue_nombre'],
                ubicacion=row['ubicacion'],
                capacidad=row['capacidad'],
                preferencia=row['preferencia'],
                costoDiario=row['costo_diario'],
                preRequisitos=row['pre_requisitos']
            )
            dueno = AnimalLoverDetalle(
                idAnimalLover=row['id_animalLover'],
                nombre=row['dueno_nombre'],
                apellido=row['apellido'],
                telefono=row['telefono'],
                email=row['email']
            )
            albergues_detalle.append(AlbergueDetalle(albergue=albergue, dueño=dueno))
        return albergues_detalle, True
    except sqlite3.Error as e:
        print(f"Error al buscar todos los albergues: {e}")
        return [], False
    finally:
        if 'conn' in locals():
            conn.close()
