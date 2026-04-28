from repositorios import alberguesRepo
from repositorios.imagenAlbergueRepo import ImagenAlbergueRepo
from manejadores import gestionMensajes
from modelos.modelos import Albergue, AlbergueDetalle
from repositorios.database import getDbConnection
import base64
from datetime import datetime

def crearAlbergue(albergue: Albergue) -> bool:
    id_albergue = alberguesRepo.guardarAlbergue(albergue)
    if id_albergue > 0:
        if albergue.imagenesBase64:
            conn = getDbConnection()
            cursor = conn.cursor()
            fecha_carga = datetime.now().isoformat()
            try:
                for img_b64 in albergue.imagenesBase64:
                    if "," in img_b64:
                        img_b64 = img_b64.split(",")[1]
                    img_bytes = base64.b64decode(img_b64)
                    consulta_img = "INSERT INTO imagen_albergue (id_albergue, imagen, fecha_carga) VALUES (?, ?, ?)"
                    cursor.execute(consulta_img, (id_albergue, img_bytes, fecha_carga))
                conn.commit()
            except Exception as e:
                print(f"Error procesando imagen de albergue: {e}")
                conn.rollback()
            finally:
                conn.close()
        return True
    return False

def obtenerTodosLosAlbergues() -> tuple[list[AlbergueDetalle], bool]:
    return alberguesRepo.buscarTodosAlbergues()

def obtenerAlbergue(id_albergue: int) -> tuple:
    return alberguesRepo.buscarAlberguePorId(id_albergue)


def actualizarAlbergue(albergue: Albergue) -> bool:
    if not albergue.idAlbergue:
        return False

    actualizado = alberguesRepo.actualizarAlbergue(albergue)
    if not actualizado:
        return False

    if albergue.imagenesBase64:
        ImagenAlbergueRepo.eliminarImagenesPorAlbergue(albergue.idAlbergue)
        conn = getDbConnection()
        cursor = conn.cursor()
        fecha_carga = datetime.now().isoformat()
        try:
            for img_b64 in albergue.imagenesBase64:
                if "," in img_b64:
                    img_b64 = img_b64.split(",")[1]
                img_bytes = base64.b64decode(img_b64)
                consulta_img = "INSERT INTO imagen_albergue (id_albergue, imagen, fecha_carga) VALUES (?, ?, ?)"
                cursor.execute(consulta_img, (albergue.idAlbergue, img_bytes, fecha_carga))
            conn.commit()
        except Exception as e:
            print(f"Error procesando imagen de albergue: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()

    return True


def eliminarAlbergue(id_albergue: int) -> bool:
    if id_albergue <= 0:
        return False

    id_trabajo_chat = -id_albergue
    gestionMensajes.eliminarMensajesPorTrabajo(id_trabajo_chat)
    ImagenAlbergueRepo.eliminarImagenesPorAlbergue(id_albergue)
    return alberguesRepo.eliminarAlbergue(id_albergue)
