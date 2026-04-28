from typing import Optional
import sqlite3

from repositorios.database import getDbConnection


class ImagenAlbergueRepo:
    @staticmethod
    def obtenerImagenPrincipal(id_albergue: int) -> Optional[bytes]:
        try:
            conn = getDbConnection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT imagen FROM imagen_albergue WHERE id_albergue = ? ORDER BY fecha_carga ASC LIMIT 1",
                (id_albergue,)
            )
            row = cursor.fetchone()
            return row["imagen"] if row else None
        except sqlite3.Error as e:
            print(f"Error al buscar imagen principal de albergue: {e}")
            return None
        finally:
            if "conn" in locals():
                conn.close()

    @staticmethod
    def contarImagenes(id_albergue: int) -> int:
        try:
            conn = getDbConnection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT COUNT(*) as total FROM imagen_albergue WHERE id_albergue = ?",
                (id_albergue,)
            )
            row = cursor.fetchone()
            return row["total"] if row else 0
        except sqlite3.Error as e:
            print(f"Error al contar imagenes de albergue: {e}")
            return 0
        finally:
            if "conn" in locals():
                conn.close()

    @staticmethod
    def obtenerImagenPorIndice(id_albergue: int, index: int) -> Optional[bytes]:
        try:
            conn = getDbConnection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT imagen FROM imagen_albergue WHERE id_albergue = ? ORDER BY fecha_carga ASC LIMIT 1 OFFSET ?",
                (id_albergue, index)
            )
            row = cursor.fetchone()
            return row["imagen"] if row else None
        except sqlite3.Error as e:
            print(f"Error al buscar imagen por indice de albergue: {e}")
            return None
        finally:
            if "conn" in locals():
                conn.close()

    @staticmethod
    def eliminarImagenesPorAlbergue(id_albergue: int) -> bool:
        try:
            conn = getDbConnection()
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM imagen_albergue WHERE id_albergue = ?",
                (id_albergue,)
            )
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error al eliminar imagenes de albergue: {e}")
            return False
        finally:
            if "conn" in locals():
                conn.close()
