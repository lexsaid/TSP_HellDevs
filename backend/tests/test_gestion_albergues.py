import base64

from manejadores import manejadorAlbergues
from modelos.modelos import Albergue


def _img_b64(data=b"img"):
    return "data:image/png;base64," + base64.b64encode(data).decode("ascii")


def test_crear_y_obtener_albergue_con_imagen(seed_user, fetch_scalar):
    # Arrange
    user = seed_user(email="albergue1@example.com", telefono="4444440000")
    albergue = Albergue(
        idAnimalLover=user.idAnimalLover,
        nombre="Casa",
        ubicacion="CDMX",
        capacidad=5,
        preferencia="Perros",
        costoDiario=30,
        preRequisitos="Req",
        imagenesBase64=[_img_b64()],
    )

    # Act
    ok = manejadorAlbergues.crearAlbergue(albergue)
    detalle, found = manejadorAlbergues.obtenerAlbergue(1)
    imagenes = fetch_scalar("SELECT COUNT(*) FROM imagen_albergue WHERE id_albergue = ?", (1,))

    # Assert
    assert ok is True
    assert found is True
    assert detalle.albergue.nombre == "Casa"
    assert imagenes == 1


def test_actualizar_albergue_reemplaza_imagenes(seed_user, fetch_scalar):
    # Arrange
    user = seed_user(email="albergue2@example.com", telefono="5555550000")
    albergue = Albergue(
        idAnimalLover=user.idAnimalLover,
        nombre="Casa2",
        ubicacion="CDMX",
        capacidad=6,
        preferencia="Perros",
        costoDiario=35,
        preRequisitos="Req",
        imagenesBase64=[_img_b64(b"a")],
    )
    manejadorAlbergues.crearAlbergue(albergue)

    actualizado = Albergue(
        idAlbergue=1,
        idAnimalLover=user.idAnimalLover,
        nombre="Casa3",
        ubicacion="CDMX",
        capacidad=7,
        preferencia="Perros",
        costoDiario=40,
        preRequisitos="Req2",
        imagenesBase64=[_img_b64(b"b"), _img_b64(b"c")],
    )

    # Act
    ok = manejadorAlbergues.actualizarAlbergue(actualizado)
    imagenes = fetch_scalar("SELECT COUNT(*) FROM imagen_albergue WHERE id_albergue = ?", (1,))

    # Assert
    assert ok is True
    assert imagenes == 2


def test_eliminar_albergue_borra_mensajes(seed_user, fetch_scalar):
    # Arrange
    user = seed_user(email="albergue3@example.com", telefono="6666660000")
    albergue = Albergue(
        idAnimalLover=user.idAnimalLover,
        nombre="Casa4",
        ubicacion="CDMX",
        capacidad=6,
        preferencia="Perros",
        costoDiario=35,
        preRequisitos="Req",
    )
    manejadorAlbergues.crearAlbergue(albergue)

    id_trabajo_chat = -1
    fetch_scalar(
        "INSERT INTO mensajes (id_animalLover_emisor, id_animalLover_receptor, id_trabajo, contenido, fecha_mensaje) VALUES (?, ?, ?, ?, ?)",
        (user.idAnimalLover, user.idAnimalLover, id_trabajo_chat, "msg", "2024-01-01"),
    )

    # Act
    ok = manejadorAlbergues.eliminarAlbergue(1)
    mensajes = fetch_scalar("SELECT COUNT(*) FROM mensajes WHERE id_trabajo = ?", (id_trabajo_chat,))

    # Assert
    assert ok is True
    assert mensajes == 0
