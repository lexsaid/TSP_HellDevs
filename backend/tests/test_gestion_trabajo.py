import base64

from manejadores import gestionTrabajo
from modelos.modelos import Trabajo


def _sample_b64(data=b"img"):
    return "data:image/png;base64," + base64.b64encode(data).decode("ascii")


def test_crear_y_obtener_trabajo_con_imagen(seed_user, fetch_scalar):
    # Arrange
    user = seed_user(email="trabajo1@example.com", telefono="5555555555")
    trabajo = Trabajo(
        nombre="Paseo",
        ubicacion="CDMX",
        fechaPublicacion="2024-01-01",
        monto=200.0,
        descripcion="Desc",
        idAnimalLoverPublicador=user.idAnimalLover,
        tipoTrabajo="Servicio",
        imagenesBase64=[_sample_b64()],
    )

    # Act
    ok = gestionTrabajo.crearTrabajo(trabajo)
    trabajo_db, found = gestionTrabajo.obtenerTrabajo(1)
    imagenes = fetch_scalar("SELECT COUNT(*) FROM imagen WHERE id_trabajo = ?", (1,))

    # Assert
    assert ok is True
    assert found is True
    assert trabajo_db.nombre == "Paseo"
    assert imagenes == 1


def test_actualizar_trabajo_reemplaza_imagenes(seed_user, fetch_scalar):
    # Arrange
    user = seed_user(email="trabajo2@example.com", telefono="6666666666")
    trabajo = Trabajo(
        nombre="Entrega",
        ubicacion="CDMX",
        fechaPublicacion="2024-01-02",
        monto=150.0,
        descripcion="Desc",
        idAnimalLoverPublicador=user.idAnimalLover,
        tipoTrabajo="Servicio",
        imagenesBase64=[_sample_b64(b"a")],
    )
    gestionTrabajo.crearTrabajo(trabajo)
    trabajo_db, _ = gestionTrabajo.obtenerTrabajo(1)

    actualizado = Trabajo(
        idTrabajo=trabajo_db.idTrabajo,
        nombre="Entrega 2",
        ubicacion="CDMX",
        fechaPublicacion="2024-01-03",
        monto=180.0,
        descripcion="Desc 2",
        idAnimalLoverPublicador=user.idAnimalLover,
        tipoTrabajo="Servicio",
        imagenesBase64=[_sample_b64(b"b"), _sample_b64(b"c")],
    )

    # Act
    ok = gestionTrabajo.actualizarTrabajo(actualizado)
    imagenes = fetch_scalar("SELECT COUNT(*) FROM imagen WHERE id_trabajo = ?", (trabajo_db.idTrabajo,))

    # Assert
    assert ok is True
    assert imagenes == 2


def test_eliminar_trabajo_elimina_dependencias(seed_user, seed_trabajo, fetch_scalar):
    # Arrange
    publicador = seed_user(email="trabajo3@example.com", telefono="7777777777")
    trabajador = seed_user(email="trabajador@example.com", telefono="8888888888")
    trabajo_id = seed_trabajo(id_publicador=publicador.idAnimalLover)

    fetch_scalar(
        "INSERT INTO imagen (id_trabajo, imagen) VALUES (?, ?)",
        (trabajo_id, b"img"),
    )
    fetch_scalar(
        "INSERT INTO mensajes (id_animalLover_emisor, id_animalLover_receptor, id_trabajo, contenido, fecha_mensaje) VALUES (?, ?, ?, ?, ?)",
        (publicador.idAnimalLover, trabajador.idAnimalLover, trabajo_id, "hola", "2024-01-01"),
    )
    fetch_scalar(
        "INSERT INTO trabajo_aceptado (id_trabajo, id_animalLover_trabajador, fecha_aceptacion, estado_trabajo) VALUES (?, ?, ?, ?)",
        (trabajo_id, trabajador.idAnimalLover, "2024-01-01", "Pendiente"),
    )

    # Act
    ok = gestionTrabajo.eliminarTrabajo(trabajo_id)
    imagenes = fetch_scalar("SELECT COUNT(*) FROM imagen WHERE id_trabajo = ?", (trabajo_id,))
    mensajes = fetch_scalar("SELECT COUNT(*) FROM mensajes WHERE id_trabajo = ?", (trabajo_id,))
    aceptados = fetch_scalar("SELECT COUNT(*) FROM trabajo_aceptado WHERE id_trabajo = ?", (trabajo_id,))

    # Assert
    assert ok is True
    assert imagenes == 0
    assert mensajes == 0
    assert aceptados == 0


def test_obtener_todos_los_trabajos(seed_trabajo):
    # Arrange
    seed_trabajo(nombre="T1")
    seed_trabajo(nombre="T2")

    # Act
    trabajos, ok = gestionTrabajo.obtenerTodosLosTrabajos()

    # Assert
    assert ok is True
    assert len(trabajos) >= 2
