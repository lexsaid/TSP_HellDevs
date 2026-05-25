import base64

from manejadores import manejadorImagenes, manejadorMasPerdidas, manejadorAlbergues
from modelos.modelos import AnimalPerdido, Albergue


def _img_b64(data=b"img"):
    return "data:image/png;base64," + base64.b64encode(data).decode("ascii")


def test_obtener_imagen_animal_y_contador(seed_user):
    # Arrange
    user = seed_user(email="img1@example.com", telefono="4444441111")
    mascota = AnimalPerdido(
        idAnimalLover=user.idAnimalLover,
        nombre="Lola",
        direccion="CDMX",
        tamanio="M",
        color="Cafe",
        discapacidad="No",
        tipoAnimal="Perro",
        edad=2,
        detallesAdicionales="Det",
        recompensa="100",
        imagenesBase64=[_img_b64(), _img_b64(b"x")],
    )
    manejadorMasPerdidas.reportarMascotaPerdida(mascota)

    # Act
    imagen, ok = manejadorImagenes.obtenerImagenAnimal(1)
    info = manejadorImagenes.obtenerInfoImagenesAnimal(1)
    imagen2, ok2 = manejadorImagenes.obtenerImagenAnimalPorIndice(1, 1)
    imagen_bad, ok_bad = manejadorImagenes.obtenerImagenAnimalPorIndice(1, -1)

    # Assert
    assert ok is True
    assert imagen is not None
    assert info["count"] == 2
    assert ok2 is True
    assert imagen2 is not None
    assert ok_bad is False
    assert imagen_bad is None


def test_obtener_imagen_albergue_y_contador(seed_user):
    # Arrange
    user = seed_user(email="img2@example.com", telefono="5555551111")
    albergue = Albergue(
        idAnimalLover=user.idAnimalLover,
        nombre="Refugio",
        ubicacion="CDMX",
        capacidad=3,
        preferencia="Perros",
        costoDiario=20,
        preRequisitos="Req",
        imagenesBase64=[_img_b64()],
    )
    manejadorAlbergues.crearAlbergue(albergue)

    # Act
    imagen, ok = manejadorImagenes.obtenerImagenAlbergue(1)
    info = manejadorImagenes.obtenerInfoImagenesAlbergue(1)
    imagen_bad, ok_bad = manejadorImagenes.obtenerImagenAlberguePorIndice(1, -1)

    # Assert
    assert ok is True
    assert imagen is not None
    assert info["count"] == 1
    assert ok_bad is False
    assert imagen_bad is None
