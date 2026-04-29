from manejadores import gestionMensajes
from modelos.modelos import Mensaje


def test_guardar_y_listar_mensajes(seed_user, seed_trabajo):
    # Arrange
    emisor = seed_user(email="emisor@example.com", telefono="1111110000")
    receptor = seed_user(email="receptor@example.com", telefono="1111110001")
    trabajo_id = seed_trabajo(id_publicador=emisor.idAnimalLover)

    mensaje = Mensaje(
        idAnimalLoverEmisor=emisor.idAnimalLover,
        idAnimalLoverReceptor=receptor.idAnimalLover,
        idTrabajo=trabajo_id,
        contenido="Hola",
        fechaMensaje="2024-01-01",
    )
    gestionMensajes.guardarMensaje(mensaje)

    # Act
    mensajes, ok = gestionMensajes.obtenerListaMensajes(emisor.idAnimalLover, receptor.idAnimalLover, trabajo_id)

    # Assert
    assert ok is True
    assert mensajes[0]["remitente"] == f"{emisor.nombre} {emisor.apellido}"
    assert mensajes[0]["receptor"] == f"{receptor.nombre} {receptor.apellido}"


def test_obtener_chats_previos_cubre_negativos(seed_user, seed_trabajo, seed_albergue, fetch_scalar):
    # Arrange
    usuario = seed_user(email="chat1@example.com", telefono="2222220000")
    otro = seed_user(email="chat2@example.com", telefono="2222220001")

    trabajo_titulo = "Trabajo"
    trabajo_id = seed_trabajo(nombre=trabajo_titulo, id_publicador=usuario.idAnimalLover)
    albergue_id = seed_albergue(id_dueno=usuario.idAnimalLover)

    # Mascota perdida
    fetch_scalar(
        "INSERT INTO animal (id_animalLover, nombre, direccion, tamanio, color, discapacidad, tipo_animal, edad, detalles_adicionales) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (usuario.idAnimalLover, "Perdido", "Dir", "M", "Cafe", "No", "Perro", 3, "Det"),
    )
    animal_id = fetch_scalar("SELECT id_animal FROM animal ORDER BY id_animal DESC LIMIT 1")
    fetch_scalar(
        "INSERT INTO animalPerdido (id_animal, recompensa, estado) VALUES (?, ?, ?)",
        (animal_id, "100", "Activo"),
    )

    # Adopcion
    fetch_scalar(
        "INSERT INTO animal (id_animalLover, nombre, direccion, tamanio, color, discapacidad, tipo_animal, edad, detalles_adicionales) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (usuario.idAnimalLover, "Adopcion", "Dir", "M", "Negro", "No", "Gato", 2, "Det"),
    )
    adopcion_id = fetch_scalar("SELECT id_animal FROM animal ORDER BY id_animal DESC LIMIT 1")
    fetch_scalar(
        "INSERT INTO animalCalle (id_animal, vacunas, estado) VALUES (?, ?, ?)",
        (adopcion_id, "Basicas", "Activo"),
    )

    mensajes = [
        Mensaje(
            idAnimalLoverEmisor=usuario.idAnimalLover,
            idAnimalLoverReceptor=otro.idAnimalLover,
            idTrabajo=trabajo_id,
            contenido="Trabajo",
            fechaMensaje="2024-01-01",
        ),
        Mensaje(
            idAnimalLoverEmisor=otro.idAnimalLover,
            idAnimalLoverReceptor=usuario.idAnimalLover,
            idTrabajo=-albergue_id,
            contenido="Albergue",
            fechaMensaje="2024-01-02",
        ),
        Mensaje(
            idAnimalLoverEmisor=otro.idAnimalLover,
            idAnimalLoverReceptor=usuario.idAnimalLover,
            idTrabajo=-1000000 - animal_id,
            contenido="Perdido",
            fechaMensaje="2024-01-03",
        ),
        Mensaje(
            idAnimalLoverEmisor=otro.idAnimalLover,
            idAnimalLoverReceptor=usuario.idAnimalLover,
            idTrabajo=-2000000 - adopcion_id,
            contenido="Adopcion",
            fechaMensaje="2024-01-04",
        ),
    ]
    for msg in mensajes:
        gestionMensajes.guardarMensaje(msg)

    # Act
    chats, ok = gestionMensajes.obtenerChatsPrevios(usuario.idAnimalLover)

    # Assert
    assert ok is True
    assert len(chats) == 4
    assert {c["tituloTrabajo"] for c in chats} >= {trabajo_titulo, "Albergue Uno", "Perdido", "Adopcion"}


def test_hay_nuevos_mensajes(seed_user, seed_trabajo):
    # Arrange
    emisor = seed_user(email="emisor2@example.com", telefono="3333330000")
    receptor = seed_user(email="receptor2@example.com", telefono="3333330001")
    trabajo_id = seed_trabajo(id_publicador=emisor.idAnimalLover)

    mensaje = Mensaje(
        idAnimalLoverEmisor=emisor.idAnimalLover,
        idAnimalLoverReceptor=receptor.idAnimalLover,
        idTrabajo=trabajo_id,
        contenido="Nuevo",
        fechaMensaje="2024-01-01",
    )
    gestionMensajes.guardarMensaje(mensaje)

    # Act
    hay = gestionMensajes.hayNuevosMensajes(receptor.idAnimalLover, 0)

    # Assert
    assert hay is True
