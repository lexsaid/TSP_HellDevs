from manejadores import gestionTrabajosAceptados
from modelos.modelos import TrabajoAceptado


def test_verificar_trabajo_aceptado_sin_registros(seed_trabajo):
    # Arrange
    trabajo_id = seed_trabajo(nombre="SinAceptado")

    # Act
    resultado = gestionTrabajosAceptados.verificarTrabajoAceptado(trabajo_id)

    # Assert
    assert resultado == {"aceptado": False, "completado": False}


def test_verificar_trabajo_aceptado_con_pendiente(seed_trabajo, seed_user):
    # Arrange
    trabajo_id = seed_trabajo(nombre="Pendiente")
    trabajador = seed_user(email="pendiente@example.com", telefono="9999999999")
    trabajo = TrabajoAceptado(
        idTrabajo=trabajo_id,
        idAnimalLoverTrabajador=trabajador.idAnimalLover,
        fechaAceptacion="2024-01-01",
        estadoTrabajo="Pendiente",
    )
    gestionTrabajosAceptados.aceptarTrabajo(trabajo)

    # Act
    resultado = gestionTrabajosAceptados.verificarTrabajoAceptado(trabajo_id)

    # Assert
    assert resultado == {"aceptado": True, "completado": False}


def test_completar_trabajo_marca_terminado(seed_trabajo, seed_user, fetch_scalar):
    # Arrange
    trabajo_id = seed_trabajo(nombre="Terminar")
    trabajador = seed_user(email="terminar@example.com", telefono="1010101010")
    trabajo = TrabajoAceptado(
        idTrabajo=trabajo_id,
        idAnimalLoverTrabajador=trabajador.idAnimalLover,
        fechaAceptacion="2024-01-01",
        estadoTrabajo="Pendiente",
    )
    gestionTrabajosAceptados.aceptarTrabajo(trabajo)

    # Act
    ok = gestionTrabajosAceptados.completarTrabajoPorPublicador(trabajo_id)
    estado = fetch_scalar(
        "SELECT estado_trabajo FROM trabajo_aceptado WHERE id_trabajo = ?",
        (trabajo_id,),
    )

    # Assert
    assert ok is True
    assert estado == "Terminado"
