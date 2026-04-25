from repositorios.database import getDbConnection
from modelos.modelos import Trabajo
import sqlite3

def guardarTrabajo(consulta: str, trabajo: Trabajo) -> int:
    try:
        conn = getDbConnection()
        cursor = conn.cursor()
        cursor.execute(consulta, (
            trabajo.nombre, 
            trabajo.ubicacion, 
            trabajo.fechaPublicacion, 
            trabajo.monto, 
            trabajo.descripcion, 
            trabajo.idAnimalLoverPublicador, 
            trabajo.tipoTrabajo
        ))
        conn.commit()
        return cursor.lastrowid
    except sqlite3.Error as e:
        print(f"Error al ejecutar la consulta en trabajo: {e}")
        return -1
    finally:
        if 'conn' in locals():
            conn.close()

def buscarIdTrabajo(consulta: str, idTrabajo: int) -> tuple[Trabajo, bool]:
    try:
        conn = getDbConnection()
        cursor = conn.cursor()
        cursor.execute(consulta, (idTrabajo,))
        row = cursor.fetchone()
        if row:
            trabajo = Trabajo(
                idTrabajo=row['id_trabajo'],
                nombre=row['nombre'],
                ubicacion=row['ubicacion'],
                fechaPublicacion=row['fecha_publicacion'],
                monto=row['monto'],
                descripcion=row['descripcion'],
                idAnimalLoverPublicador=row['id_animalLover_publicador'],
                tipoTrabajo=row['tipo_trabajo']
            )
            return trabajo, True
        return None, False
    except sqlite3.Error as e:
        print(f"Error al buscar el trabajo: {e}")
        return None, False
    finally:
        if 'conn' in locals():
            conn.close()

def actualizarTrabajo(consulta: str, trabajo: Trabajo) -> bool:
    try:
        conn = getDbConnection()
        cursor = conn.cursor()
        cursor.execute(consulta, (
            trabajo.nombre, 
            trabajo.ubicacion, 
            trabajo.fechaPublicacion, 
            trabajo.monto, 
            trabajo.descripcion, 
            trabajo.idAnimalLoverPublicador, 
            trabajo.tipoTrabajo, 
            trabajo.idTrabajo
        ))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error al actualizar la consulta en trabajo: {e}")
        return False
    finally:
        if 'conn' in locals():
            conn.close()

def eliminarTrabajo(consulta: str, idTrabajo: int) -> bool:
    try:
        conn = getDbConnection()
        cursor = conn.cursor()
        
        # Cascade delete manually
        cursor.execute("DELETE FROM imagen WHERE id_trabajo = ?", (idTrabajo,))
        cursor.execute("DELETE FROM mensajes WHERE id_trabajo = ?", (idTrabajo,))
        cursor.execute("DELETE FROM trabajo_aceptado WHERE id_trabajo = ?", (idTrabajo,))
        
        cursor.execute(consulta, (idTrabajo,))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error al eliminar la consulta en trabajo: {e}")
        return False
    finally:
        if 'conn' in locals():
            conn.close()

def buscarTodosTrabajos(consulta: str) -> tuple[list[Trabajo], bool]:
    try:
        conn = getDbConnection()
        cursor = conn.cursor()
        cursor.execute(consulta)
        rows = cursor.fetchall()
        trabajos = []
        for row in rows:
            trabajo = Trabajo(
                idTrabajo=row['id_trabajo'],
                nombre=row['nombre'],
                ubicacion=row['ubicacion'],
                fechaPublicacion=row['fecha_publicacion'],
                monto=row['monto'],
                descripcion=row['descripcion'],
                idAnimalLoverPublicador=row['id_animalLover_publicador'],
                tipoTrabajo=row['tipo_trabajo']
            )
            trabajos.append(trabajo)
        return trabajos, True
    except sqlite3.Error as e:
        print(f"Error al buscar todos los trabajos: {e}")
        return [], False
    finally:
        if 'conn' in locals():
            conn.close()

