from repositorios import trabajosAceptadosRepo
from modelos.modelos import TrabajoAceptado

def aceptarTrabajo(trabajo: TrabajoAceptado) -> bool:
    consulta = "INSERT INTO trabajo_aceptado (id_trabajo, id_animalLover_trabajador, fecha_aceptacion, estado_trabajo) VALUES (?, ?, ?, ?)"
    return trabajosAceptadosRepo.guardarTrabajoAceptado(consulta, trabajo)

def obtenerListaTrabajosAceptados(idUsuario: int) -> tuple[list[TrabajoAceptado], bool]:
    consulta = "SELECT * FROM trabajo_aceptado WHERE id_animalLover_trabajador = ?"
    return trabajosAceptadosRepo.buscarIdUsuarioTrabajo(consulta, idUsuario)

def actualizarTrabajoAceptado(trabajo: TrabajoAceptado) -> bool:
    consulta = "UPDATE trabajo_aceptado SET fecha_aceptacion = ?, estado_trabajo = ? WHERE id_trabajo = ? AND id_animalLover_trabajador = ?"
    return trabajosAceptadosRepo.actualizarTrabajoAceptado(consulta, trabajo)

def eliminarTrabajoAceptado(idTrabajo: int, idAnimalLoverTrabajador: int) -> bool:
    consulta = "DELETE FROM trabajo_aceptado WHERE id_trabajo = ? AND id_animalLover_trabajador = ?"
    return trabajosAceptadosRepo.eliminarTrabajoAceptado(consulta, idTrabajo, idAnimalLoverTrabajador)

def verificarTrabajoAceptado(idTrabajo: int) -> dict:
    """Retorna info sobre el estado de aceptación del trabajo."""
    consulta = "SELECT * FROM trabajo_aceptado WHERE id_trabajo = ?"
    lista, ok = trabajosAceptadosRepo.buscarPorTrabajo(consulta, idTrabajo)
    if not ok or len(lista) == 0:
        return {"aceptado": False, "completado": False}
    
    completado = any(t.estadoTrabajo == "Terminado" for t in lista)
    aceptado = any(t.estadoTrabajo == "Pendiente" for t in lista)
    return {"aceptado": aceptado or completado, "completado": completado}

def completarTrabajoPorPublicador(idTrabajo: int) -> bool:
    """Actualiza el registro del trabajador que aceptó el trabajo a estado Terminado."""
    consulta = "UPDATE trabajo_aceptado SET estado_trabajo = 'Terminado' WHERE id_trabajo = ? AND estado_trabajo = 'Pendiente'"
    return trabajosAceptadosRepo.completarTrabajo(consulta, idTrabajo)
