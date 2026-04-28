from typing import Optional
import sqlite3

from repositorios.database import getDbConnection


class ImagenAnimalRepo:
    @staticmethod
    def obtenerImagenPrincipal(id_animal: int) -> Optional[bytes]:
        try:
            conn = getDbConnection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT imagen FROM imagen_animal WHERE id_animal = ? ORDER BY fecha_carga ASC LIMIT 1",
                (id_animal,)
            )
            row = cursor.fetchone()
            return row["imagen"] if row else None
        except sqlite3.Error as e:
            print(f"Error al buscar imagen principal de animal: {e}")
            return None
        finally:
            if "conn" in locals():
                conn.close()

    @staticmethod
    def contarImagenes(id_animal: int) -> int:
        try:
            conn = getDbConnection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT COUNT(*) as total FROM imagen_animal WHERE id_animal = ?",
                (id_animal,)
            )
            row = cursor.fetchone()
            return row["total"] if row else 0
        except sqlite3.Error as e:
            print(f"Error al contar imagenes de animal: {e}")
            return 0
        finally:
            if "conn" in locals():
                conn.close()

    @staticmethod
    def obtenerImagenPorIndice(id_animal: int, index: int) -> Optional[bytes]:
        try:
            conn = getDbConnection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT imagen FROM imagen_animal WHERE id_animal = ? ORDER BY fecha_carga ASC LIMIT 1 OFFSET ?",
                (id_animal, index)
            )
            row = cursor.fetchone()
            return row["imagen"] if row else None
        except sqlite3.Error as e:
            print(f"Error al buscar imagen por indice de animal: {e}")
            return None
        finally:
            if "conn" in locals():
                conn.close()

    @staticmethod
    def eliminarImagenesPorAnimal(id_animal: int) -> bool:
        try:
            conn = getDbConnection()
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM imagen_animal WHERE id_animal = ?",
                (id_animal,)
            )
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error al eliminar imagenes de animal: {e}")
            return False
        finally:
            if "conn" in locals():
                conn.close()
