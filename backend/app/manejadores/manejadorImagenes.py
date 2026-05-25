from typing import Optional

from repositorios.imagenAlbergueRepo import ImagenAlbergueRepo
from repositorios.imagenAnimalRepo import ImagenAnimalRepo


def obtenerImagenAnimal(id_animal: int) -> tuple[Optional[bytes], bool]:
    imagen = ImagenAnimalRepo.obtenerImagenPrincipal(id_animal)
    if not imagen:
        return None, False
    return imagen, True


def obtenerInfoImagenesAnimal(id_animal: int) -> dict:
    total = ImagenAnimalRepo.contarImagenes(id_animal)
    return {"count": total}


def obtenerImagenAnimalPorIndice(id_animal: int, index: int) -> tuple[Optional[bytes], bool]:
    if index < 0:
        return None, False
    imagen = ImagenAnimalRepo.obtenerImagenPorIndice(id_animal, index)
    if not imagen:
        return None, False
    return imagen, True


def obtenerImagenAlbergue(id_albergue: int) -> tuple[Optional[bytes], bool]:
    imagen = ImagenAlbergueRepo.obtenerImagenPrincipal(id_albergue)
    if not imagen:
        return None, False
    return imagen, True


def obtenerInfoImagenesAlbergue(id_albergue: int) -> dict:
    total = ImagenAlbergueRepo.contarImagenes(id_albergue)
    return {"count": total}


def obtenerImagenAlberguePorIndice(id_albergue: int, index: int) -> tuple[Optional[bytes], bool]:
    if index < 0:
        return None, False
    imagen = ImagenAlbergueRepo.obtenerImagenPorIndice(id_albergue, index)
    if not imagen:
        return None, False
    return imagen, True
