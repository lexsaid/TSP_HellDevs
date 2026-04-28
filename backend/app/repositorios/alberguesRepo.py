from repositorios.database import getDbConnection
from modelos.modelos import Albergue, AlbergueDetalle, AnimalLoverDetalle
from typing import Optional
import sqlite3


def guardarAlbergue(albergue: Albergue) -> int:
    """
    Inserta un nuevo albergue en la base de datos.
    Retorna el id_albergue generado, o -1 si hubo un error.
    """
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

        id_albergue = cursor.lastrowid
        conn.commit()
        return id_albergue
    except sqlite3.Error as e:
        if 'conn' in locals():
            conn.rollback()
        print(f"Error al guardar Albergue: {e}")
        return -1
    finally:
        if 'conn' in locals():
            conn.close()


def buscarTodosAlbergues() -> tuple[list[AlbergueDetalle], bool]:
    """
    Obtiene todos los albergues registrados junto con los datos del dueño (AnimalLover).
    Retorna una tupla (lista_de_detalles, éxito).
    """
    try:
        conn = getDbConnection()
        cursor = conn.cursor()

        consulta = """
            SELECT
                alb.id_albergue, alb.id_animalLover, alb.nombre as albergue_nombre,
                alb.ubicacion, alb.capacidad, alb.preferencia, alb.costo_diario, alb.pre_requisitos,
                al.nombre as dueno_nombre, al.apellido, al.telefono, al.email
            FROM albergue alb
            INNER JOIN animalLover al ON alb.id_animalLover = al.id_animalLover
            ORDER BY alb.id_albergue DESC
        """
        cursor.execute(consulta)
        rows = cursor.fetchall()

        detalles = []
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
            detalles.append(AlbergueDetalle(albergue=albergue, dueño=dueno))

        return detalles, True
    except sqlite3.Error as e:
        print(f"Error al buscar todos los albergues: {e}")
        return [], False
    finally:
        if 'conn' in locals():
            conn.close()


def buscarAlberguePorId(id_albergue: int) -> tuple[Optional[AlbergueDetalle], bool]:
    """
    Obtiene un albergue específico junto con los datos del dueño.
    Retorna (AlbergueDetalle, True) o (None, False).
    """
    try:
        conn = getDbConnection()
        cursor = conn.cursor()
        consulta = """
            SELECT
                alb.id_albergue, alb.id_animalLover, alb.nombre as albergue_nombre,
                alb.ubicacion, alb.capacidad, alb.preferencia, alb.costo_diario, alb.pre_requisitos,
                al.nombre as dueno_nombre, al.apellido, al.telefono, al.email
            FROM albergue alb
            INNER JOIN animalLover al ON alb.id_animalLover = al.id_animalLover
            WHERE alb.id_albergue = ?
        """
        cursor.execute(consulta, (id_albergue,))
        row = cursor.fetchone()
        if not row:
            return None, False
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
        return AlbergueDetalle(albergue=albergue, dueño=dueno), True
    except sqlite3.Error as e:
        print(f"Error al buscar albergue por id: {e}")
        return None, False
    finally:
        if 'conn' in locals():
            conn.close()


def actualizarAlbergue(albergue: Albergue) -> bool:
    try:
        conn = getDbConnection()
        cursor = conn.cursor()
        consulta = """
            UPDATE albergue
            SET nombre = ?, ubicacion = ?, capacidad = ?, preferencia = ?, costo_diario = ?, pre_requisitos = ?
            WHERE id_albergue = ?
        """
        cursor.execute(consulta, (
            albergue.nombre,
            albergue.ubicacion,
            albergue.capacidad,
            albergue.preferencia,
            albergue.costoDiario,
            albergue.preRequisitos,
            albergue.idAlbergue
        ))
        conn.commit()
        return cursor.rowcount > 0
    except sqlite3.Error as e:
        if 'conn' in locals():
            conn.rollback()
        print(f"Error al actualizar Albergue: {e}")
        return False
    finally:
        if 'conn' in locals():
            conn.close()


def eliminarAlbergue(id_albergue: int) -> bool:
    try:
        conn = getDbConnection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM albergue WHERE id_albergue = ?", (id_albergue,))
        conn.commit()
        return cursor.rowcount > 0
    except sqlite3.Error as e:
        if 'conn' in locals():
            conn.rollback()
        print(f"Error al eliminar Albergue: {e}")
        return False
    finally:
        if 'conn' in locals():
            conn.close()

