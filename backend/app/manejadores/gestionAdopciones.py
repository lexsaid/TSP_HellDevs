from repositorios import adopcionesRepo
from repositorios.imagenAnimalRepo import ImagenAnimalRepo
from manejadores import gestionMensajes
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


def obtenerAdopcionesPorUsuario(id_animalLover: int) -> tuple[list[AdopcionDetalle], bool]:
    return adopcionesRepo.buscarAdopcionesPorUsuario(id_animalLover)


def obtenerAdopcion(id_animal: int) -> tuple:
    return adopcionesRepo.buscarAdopcionPorId(id_animal)


def actualizarAdopcion(adopcion: AnimalCalle) -> bool:
    if not adopcion.idAnimal:
        return False

    actualizado = adopcionesRepo.actualizarAdopcion(adopcion)
    if not actualizado:
        return False

    if adopcion.imagenesBase64:
        ImagenAnimalRepo.eliminarImagenesPorAnimal(adopcion.idAnimal)
        conn = getDbConnection()
        cursor = conn.cursor()
        fecha_carga = datetime.now().isoformat()
        try:
            for img_b64 in adopcion.imagenesBase64:
                if "," in img_b64:
                    img_b64 = img_b64.split(",")[1]
                img_bytes = base64.b64decode(img_b64)
                consulta_img = "INSERT INTO imagen_animal (id_animal, imagen, fecha_carga) VALUES (?, ?, ?)"
                cursor.execute(consulta_img, (adopcion.idAnimal, img_bytes, fecha_carga))
            conn.commit()
        except Exception as e:
            print(f"Error procesando imagen de adopcion: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()

    return True


def marcarAdopcionAdoptada(id_animal: int) -> bool:
    return adopcionesRepo.actualizarEstadoAdopcion(id_animal, "Adoptado")


def eliminarAdopcion(id_animal: int) -> bool:
    if id_animal <= 0:
        return False

    id_trabajo_chat = -2000000 - id_animal
    gestionMensajes.eliminarMensajesPorTrabajo(id_trabajo_chat)
    return adopcionesRepo.eliminarAdopcion(id_animal)
