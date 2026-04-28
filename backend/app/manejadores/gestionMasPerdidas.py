from repositorios import mascotasPerdidasRepo
from repositorios.imagenAnimalRepo import ImagenAnimalRepo
from manejadores import gestionMensajes
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


def obtenerMascotasPerdidasPorUsuario(id_animalLover: int) -> tuple[list[MascotaPerdidaDetalle], bool]:
    return mascotasPerdidasRepo.buscarMascotasPerdidasPorUsuario(id_animalLover)


def obtenerMascotaPerdida(id_animal: int) -> tuple:
    return mascotasPerdidasRepo.buscarMascotaPerdidaPorId(id_animal)


def actualizarMascotaPerdida(mascota: AnimalPerdido) -> bool:
    if not mascota.idAnimal:
        return False

    actualizado = mascotasPerdidasRepo.actualizarMascotaPerdida(mascota)
    if not actualizado:
        return False

    if mascota.imagenesBase64:
        ImagenAnimalRepo.eliminarImagenesPorAnimal(mascota.idAnimal)
        conn = getDbConnection()
        cursor = conn.cursor()
        fecha_carga = datetime.now().isoformat()
        try:
            for img_b64 in mascota.imagenesBase64:
                if "," in img_b64:
                    img_b64 = img_b64.split(",")[1]
                img_bytes = base64.b64decode(img_b64)
                consulta_img = "INSERT INTO imagen_animal (id_animal, imagen, fecha_carga) VALUES (?, ?, ?)"
                cursor.execute(consulta_img, (mascota.idAnimal, img_bytes, fecha_carga))
            conn.commit()
        except Exception as e:
            print(f"Error procesando imagen de mascota perdida: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()

    return True


def marcarMascotaLocalizada(id_animal: int) -> bool:
    return mascotasPerdidasRepo.actualizarEstadoMascotaPerdida(id_animal, "Localizado")


def eliminarMascotaPerdida(id_animal: int) -> bool:
    if id_animal <= 0:
        return False

    id_trabajo_chat = -1000000 - id_animal
    gestionMensajes.eliminarMensajesPorTrabajo(id_trabajo_chat)
    return mascotasPerdidasRepo.eliminarMascotaPerdida(id_animal)
