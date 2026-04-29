import base64

from manejadores import gestionMasPerdidas
from modelos.modelos import AnimalPerdido


def _img_b64(data=b"img"):
    return "data:image/png;base64," + base64.b64encode(data).decode("ascii")


def test_reportar_y_obtener_mascota(seed_user, fetch_scalar):
    # Arrange
    user = seed_user(email="perdida1@example.com", telefono="7777770000")
    mascota = AnimalPerdido(
        idAnimalLover=user.idAnimalLover,
        nombre="Firulais",
        direccion="CDMX",
        tamanio="M",
        color="Cafe",
        discapacidad="No",
        tipoAnimal="Perro",
        edad=3,
        detallesAdicionales="Det",
        recompensa="100",
        imagenesBase64=[_img_b64()],
    )

    # Act
    ok = gestionMasPerdidas.reportarMascotaPerdida(mascota)
    detalle, found = gestionMasPerdidas.obtenerMascotaPerdida(1)
    imagenes = fetch_scalar("SELECT COUNT(*) FROM imagen_animal WHERE id_animal = ?", (1,))

    # Assert
    assert ok is True
    assert found is True
    assert detalle.mascotaPerdida.nombre == "Firulais"
    assert imagenes == 1


def test_actualizar_mascota_reemplaza_imagenes(seed_user, fetch_scalar):
    # Arrange
    user = seed_user(email="perdida2@example.com", telefono="8888880000")
    mascota = AnimalPerdido(
        idAnimalLover=user.idAnimalLover,
        nombre="Bolt",
        direccion="CDMX",
        tamanio="M",
        color="Blanco",
        discapacidad="No",
        tipoAnimal="Perro",
        edad=4,
        detallesAdicionales="Det",
        recompensa="150",
        imagenesBase64=[_img_b64(b"a")],
    )
    gestionMasPerdidas.reportarMascotaPerdida(mascota)

    actualizada = AnimalPerdido(
        idAnimal=1,
        idAnimalLover=user.idAnimalLover,
        nombre="Bolt2",
        direccion="CDMX",
        tamanio="G",
        color="Negro",
        discapacidad="No",
        tipoAnimal="Perro",
        edad=5,
        detallesAdicionales="Det2",
        recompensa="200",
        imagenesBase64=[_img_b64(b"b"), _img_b64(b"c")],
    )

    # Act
    ok = gestionMasPerdidas.actualizarMascotaPerdida(actualizada)
    imagenes = fetch_scalar("SELECT COUNT(*) FROM imagen_animal WHERE id_animal = ?", (1,))

    # Assert
    assert ok is True
    assert imagenes == 2


def test_marcar_localizada_y_eliminar(seed_user, fetch_scalar):
    # Arrange
    user = seed_user(email="perdida3@example.com", telefono="9999990000")
    mascota = AnimalPerdido(
        idAnimalLover=user.idAnimalLover,
        nombre="Luna",
        direccion="CDMX",
        tamanio="C",
        color="Negro",
        discapacidad="No",
        tipoAnimal="Gato",
        edad=2,
        detallesAdicionales="Det",
        recompensa="0",
    )
    gestionMasPerdidas.reportarMascotaPerdida(mascota)

    id_trabajo_chat = -1000000 - 1
    fetch_scalar(
        "INSERT INTO mensajes (id_animalLover_emisor, id_animalLover_receptor, id_trabajo, contenido, fecha_mensaje) VALUES (?, ?, ?, ?, ?)",
        (user.idAnimalLover, user.idAnimalLover, id_trabajo_chat, "msg", "2024-01-01"),
    )

    # Act
    localizado = gestionMasPerdidas.marcarMascotaLocalizada(1)
    eliminado = gestionMasPerdidas.eliminarMascotaPerdida(1)
    mensajes = fetch_scalar("SELECT COUNT(*) FROM mensajes WHERE id_trabajo = ?", (id_trabajo_chat,))

    # Assert
    assert localizado is True
    assert eliminado is True
    assert mensajes == 0
