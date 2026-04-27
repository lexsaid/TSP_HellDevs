from repositorios import adopcionesRepo
from modelos.modelos import AnimalCalle, AdopcionDetalle
from repositorios.database import getDbConnection
import base64
from datetime import datetime

def publicarAdopcion(adopcion: AnimalCalle) -> bool:
    id_animal = adopcionesRepo.guardarAdopcion(adopcion)
    if id_animal > 0:
        if adopcion.imagenesBase64:
            conn = getDbConnection()
            cursor = conn.cursor()
            fecha_carga = datetime.now().isoformat()
            try:
                for img_b64 in adopcion.imagenesBase64:
                    if "," in img_b64:
                        img_b64 = img_b64.split(",")[1]
                    img_bytes = base64.b64decode(img_b64)
                    consulta_img = "INSERT INTO imagen_animal (id_animal, imagen, fecha_carga) VALUES (?, ?, ?)"
                    cursor.execute(consulta_img, (id_animal, img_bytes, fecha_carga))
                conn.commit()
            except Exception as e:
                print(f"Error procesando imagen de adopción: {e}")
                conn.rollback()
            finally:
                conn.close()
        return True
    return False

def obtenerAdopciones() -> tuple[list[AdopcionDetalle], bool]:
    return adopcionesRepo.buscarTodasAdopciones()
