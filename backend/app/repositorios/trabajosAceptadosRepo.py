from repositorios.database import getDbConnection
from modelos.modelos import TrabajoAceptado
import sqlite3

def guardarTrabajoAceptado(consulta: str, trabajo: TrabajoAceptado) -> bool:
    try:
        conn = getDbConnection()
        cursor = conn.cursor()
        cursor.execute(consulta, (
            trabajo.idTrabajo, 
            trabajo.idAnimalLoverTrabajador, 
            trabajo.fechaAceptacion, 
            trabajo.estadoTrabajo
        ))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error al ejecutar la consulta en trabajos aceptados: {e}")
        return False
    finally:
        if 'conn' in locals():
            conn.close()

def buscarIdUsuarioTrabajo(consulta: str, idUsuario: int) -> tuple[list[TrabajoAceptado], bool]:
    try:
        conn = getDbConnection()
        cursor = conn.cursor()
        cursor.execute(consulta, (idUsuario,))
        rows = cursor.fetchall()
        
        listaTrabajosAceptados = []
        for row in rows:
            trabajo = TrabajoAceptado(
                idTrabajo=row['id_trabajo'],
                idAnimalLoverTrabajador=row['id_animalLover_trabajador'],
                fechaAceptacion=row['fecha_aceptacion'],
                estadoTrabajo=row['estado_trabajo']
            )
            listaTrabajosAceptados.append(trabajo)
            
        return listaTrabajosAceptados, True
    except sqlite3.Error as e:
        print(f"Error al buscar el trabajo aceptado: {e}")
        return [], False
    finally:
        if 'conn' in locals():
            conn.close()

def actualizarTrabajoAceptado(consulta: str, trabajo: TrabajoAceptado) -> bool:
    try:
        conn = getDbConnection()
        cursor = conn.cursor()
        # Asumiendo que actualiza por los dos IDs (llave compuesta)
        cursor.execute(consulta, (
            trabajo.fechaAceptacion,
            trabajo.estadoTrabajo,
            trabajo.idTrabajo,
            trabajo.idAnimalLoverTrabajador
        ))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error al actualizar la consulta en trabajos aceptados: {e}")
        return False
    finally:
        if 'conn' in locals():
            conn.close()

def eliminarTrabajoAceptado(consulta: str, idTrabajo: int, idAnimalLoverTrabajador: int) -> bool:
    try:
        conn = getDbConnection()
        cursor = conn.cursor()
        cursor.execute(consulta, (idTrabajo, idAnimalLoverTrabajador))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error al eliminar en trabajos aceptados: {e}")
        return False
    finally:
        if 'conn' in locals():
            conn.close()

def buscarPorTrabajo(consulta: str, idTrabajo: int) -> tuple[list, bool]:
    try:
        conn = getDbConnection()
        cursor = conn.cursor()
        cursor.execute(consulta, (idTrabajo,))
        rows = cursor.fetchall()
        
        lista = []
        for row in rows:
            trabajo = TrabajoAceptado(
                idTrabajo=row['id_trabajo'],
                idAnimalLoverTrabajador=row['id_animalLover_trabajador'],
                fechaAceptacion=row['fecha_aceptacion'],
                estadoTrabajo=row['estado_trabajo']
            )
            lista.append(trabajo)
            
        return lista, True
    except sqlite3.Error as e:
        print(f"Error al buscar trabajos aceptados por trabajo: {e}")
        return [], False
    finally:
        if 'conn' in locals():
            conn.close()

def completarTrabajo(consulta: str, idTrabajo: int) -> bool:
    try:
        conn = getDbConnection()
        cursor = conn.cursor()
        cursor.execute(consulta, (idTrabajo,))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error al completar trabajo: {e}")
        return False
    finally:
        if 'conn' in locals():
            conn.close()
