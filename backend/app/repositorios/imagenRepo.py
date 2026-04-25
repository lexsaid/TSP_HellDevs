from repositorios.database import getDbConnection
from modelos.modelos import Imagen
import sqlite3

def guardarImagen(consulta: str, imagen: Imagen) -> bool:
    try:
        conn = getDbConnection()
        cursor = conn.cursor()
        cursor.execute(consulta, (imagen.idTrabajo, imagen.imagen))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error al ejecutar la consulta en imagen: {e}")
        return False
    finally:
        if 'conn' in locals():
            conn.close()

def buscarImagenes(consulta: str, idTrabajo: int) -> tuple[list[Imagen], bool]:
    try:
        conn = getDbConnection()
        cursor = conn.cursor()
        cursor.execute(consulta, (idTrabajo,))
        rows = cursor.fetchall()
        
        imagenes = []
        for row in rows:
            img = Imagen(
                idImagen=row['id_imagen'],
                idTrabajo=row['id_trabajo'],
                imagen=row['imagen']
            )
            imagenes.append(img)
            
        return imagenes, True
    except sqlite3.Error as e:
        print(f"Error al buscar la imagen: {e}")
        return [], False
    finally:
        if 'conn' in locals():
            conn.close()

def actualizarImagen(consulta: str, imagen: Imagen) -> bool:
    try:
        conn = getDbConnection()
        cursor = conn.cursor()
        cursor.execute(consulta, (imagen.idTrabajo, imagen.imagen, imagen.idImagen))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error al actualizar la consulta en imagen: {e}")
        return False
    finally:
        if 'conn' in locals():
            conn.close()

def eliminarImagen(consulta: str, idImagen: int) -> bool:
    try:
        conn = getDbConnection()
        cursor = conn.cursor()
        cursor.execute(consulta, (idImagen,))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error al eliminar la consulta en imagen: {e}")
        return False
    finally:
        if 'conn' in locals():
            conn.close()

def eliminarImagenesPorTrabajo(idTrabajo: int) -> bool:
    try:
        conn = getDbConnection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM imagen WHERE id_trabajo = ?", (idTrabajo,))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error al eliminar imágenes por trabajo: {e}")
        return False
    finally:
        if 'conn' in locals():
            conn.close()
