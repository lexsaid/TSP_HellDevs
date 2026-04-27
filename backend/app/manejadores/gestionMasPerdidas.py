from repositorios import mascotasPerdidasRepo
from modelos.modelos import AnimalPerdido, MascotaPerdidaDetalle
from repositorios.database import getDbConnection
import base64
from datetime import datetime

def reportarMascotaPerdida(mascota: AnimalPerdido) -> bool:
    id_animal = mascotasPerdidasRepo.guardarMascotaPerdida(mascota)
    if id_animal > 0:
        if mascota.imagenesBase64:
            conn = getDbConnection()
            cursor = conn.cursor()
            fecha_carga = datetime.now().isoformat()
            try:
                for img_b64 in mascota.imagenesBase64:
                    if "," in img_b64:
                        img_b64 = img_b64.split(",")[1]
                    img_bytes = base64.b64decode(img_b64)
                    consulta_img = "INSERT INTO imagen_animal (id_animal, imagen, fecha_carga) VALUES (?, ?, ?)"
                    cursor.execute(consulta_img, (id_animal, img_bytes, fecha_carga))
                conn.commit()
            except Exception as e:
                print(f"Error procesando imagen de mascota perdida: {e}")
                conn.rollback()
            finally:
                conn.close()
        return True
    return False

def obtenerMascotasPerdidas() -> tuple[list[MascotaPerdidaDetalle], bool]:
    return mascotasPerdidasRepo.buscarTodasMascotasPerdidas()
