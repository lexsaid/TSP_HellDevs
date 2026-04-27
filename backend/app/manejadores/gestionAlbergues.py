from repositorios import alberguesRepo
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
