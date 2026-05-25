import base64

from manejadores import manejadorAdopciones
from modelos.modelos import AnimalCalle


def _img_b64(data=b"img"):
    return "data:image/png;base64," + base64.b64encode(data).decode("ascii")


def test_publicar_y_obtener_adopcion(seed_user, fetch_scalar):
    # Arrange
    user = seed_user(email="adop1@example.com", telefono="1111112222")
    adopcion = AnimalCalle(
        idAnimalLover=user.idAnimalLover,
        nombre="Milo",
        direccion="CDMX",
        tamanio="M",
        color="Blanco",
        discapacidad="No",
        tipoAnimal="Gato",
        edad=1,
        detallesAdicionales="Det",
        vacunas="Basicas",
        imagenesBase64=[_img_b64()],
    )

    # Act
    ok = manejadorAdopciones.publicarAdopcion(adopcion)
    detalle, found = manejadorAdopciones.obtenerAdopcion(1)
    imagenes = fetch_scalar("SELECT COUNT(*) FROM imagen_animal WHERE id_animal = ?", (1,))

    # Assert
    assert ok is True
    assert found is True
    assert detalle.adopcion.nombre == "Milo"
    assert imagenes == 1


def test_actualizar_adopcion_reemplaza_imagenes(seed_user, fetch_scalar):
    # Arrange
    user = seed_user(email="adop2@example.com", telefono="2222223333")
    adopcion = AnimalCalle(
        idAnimalLover=user.idAnimalLover,
        nombre="Nina",
        direccion="CDMX",
        tamanio="C",
        color="Negro",
        discapacidad="No",
        tipoAnimal="Gato",
        edad=2,
        detallesAdicionales="Det",
        vacunas="Basicas",
        imagenesBase64=[_img_b64(b"a")],
    )
    manejadorAdopciones.publicarAdopcion(adopcion)

    actualizada = AnimalCalle(
        idAnimal=1,
        idAnimalLover=user.idAnimalLover,
        nombre="Nina2",
        direccion="CDMX",
        tamanio="G",
        color="Cafe",
        discapacidad="No",
        tipoAnimal="Gato",
        edad=3,
        detallesAdicionales="Det2",
        vacunas="Completa",
        imagenesBase64=[_img_b64(b"b"), _img_b64(b"c")],
    )

    # Act
    ok = manejadorAdopciones.actualizarAdopcion(actualizada)
    imagenes = fetch_scalar("SELECT COUNT(*) FROM imagen_animal WHERE id_animal = ?", (1,))

    # Assert
    assert ok is True
    assert imagenes == 2


def test_marcar_adoptado_y_eliminar(seed_user, fetch_scalar):
    # Arrange
    user = seed_user(email="adop3@example.com", telefono="3333334444")
    adopcion = AnimalCalle(
        idAnimalLover=user.idAnimalLover,
        nombre="Max",
        direccion="CDMX",
        tamanio="M",
        color="Gris",
        discapacidad="No",
        tipoAnimal="Perro",
        edad=4,
        detallesAdicionales="Det",
        vacunas="Basicas",
    )
    manejadorAdopciones.publicarAdopcion(adopcion)

    id_trabajo_chat = -2000000 - 1
    fetch_scalar(
        "INSERT INTO mensajes (id_animalLover_emisor, id_animalLover_receptor, id_trabajo, contenido, fecha_mensaje) VALUES (?, ?, ?, ?, ?)",
        (user.idAnimalLover, user.idAnimalLover, id_trabajo_chat, "msg", "2024-01-01"),
    )

    # Act
    adoptado = manejadorAdopciones.marcarAdopcionAdoptada(1)
    eliminado = manejadorAdopciones.eliminarAdopcion(1)
    mensajes = fetch_scalar("SELECT COUNT(*) FROM mensajes WHERE id_trabajo = ?", (id_trabajo_chat,))

    # Assert
    assert adoptado is True
    assert eliminado is True
    assert mensajes == 0
