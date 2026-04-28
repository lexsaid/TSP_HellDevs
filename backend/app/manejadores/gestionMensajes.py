from repositorios import mensajesRepo
from manejadores import gestionUsuario
from modelos.modelos import Mensaje

def guardarMensaje(mensaje: Mensaje) -> bool:
    consulta = "INSERT INTO mensajes (id_animalLover_emisor, id_animalLover_receptor, id_trabajo, contenido, fecha_mensaje) VALUES (?, ?, ?, ?, ?)"
    return mensajesRepo.guardarMensaje(consulta, mensaje)

def obtenerListaMensajes(idUsuario: int, idOtroUsuario: int, idTrabajo: int) -> tuple[list[dict], bool]:
    consulta = """
        SELECT * FROM mensajes
        WHERE id_trabajo = ?
          AND (
            (id_animalLover_emisor = ? AND id_animalLover_receptor = ?)
            OR
            (id_animalLover_emisor = ? AND id_animalLover_receptor = ?)
          )
        ORDER BY fecha_mensaje ASC
    """
    mensajes, ok = mensajesRepo.buscarMensajes(consulta, idUsuario, idOtroUsuario, idTrabajo)
    if not ok:
        return [], False
    
    listaFinal = []
    for msj in mensajes:
        remitente, _ = gestionUsuario.buscarUsuario(msj.idAnimalLoverEmisor)
        receptor, _ = gestionUsuario.buscarUsuario(msj.idAnimalLoverReceptor)
        
        nombreRemitente = f"{remitente.nombre} {remitente.apellido}" if remitente else "Desconocido"
        nombreReceptor = f"{receptor.nombre} {receptor.apellido}" if receptor else "Desconocido"
        
        listaFinal.append({
            "idMensaje": msj.idMensaje,
            "remitente": nombreRemitente,
            "idRemitente": msj.idAnimalLoverEmisor,
            "receptor": nombreReceptor,
            "idReceptor": msj.idAnimalLoverReceptor,
            "idTrabajo": msj.idTrabajo,
            "contenido": msj.contenido,
            "fechaMensaje": msj.fechaMensaje
        })
        
    return listaFinal, True

def actualizarMensaje(idMensaje: int, contenido: str) -> bool:
    consulta = "UPDATE mensajes SET contenido = ? WHERE id_mensaje = ?"
    return mensajesRepo.actualizarMensaje(consulta, idMensaje, contenido)

def eliminarMensaje(idMensaje: int) -> bool:
    consulta = "DELETE FROM mensajes WHERE id_mensaje = ?"
    return mensajesRepo.eliminarMensaje(consulta, idMensaje)

def obtenerChatsPrevios(idUsuario: int) -> tuple[list[dict], bool]:
    from manejadores import gestionTrabajo
    consulta = "SELECT * FROM mensajes WHERE id_animalLover_emisor = ? OR id_animalLover_receptor = ? ORDER BY fecha_mensaje DESC"
    mensajes, ok = mensajesRepo.buscarMensajesPorUsuario(consulta, idUsuario)
    if not ok:
        return [], False
    
    # Agrupar por (idTrabajo, otherUser)
    # chats_map guarda: el mensaje más reciente (para fecha) y el último mensaje del otro usuario (para preview)
    chats_map = {}
    for msj in mensajes:
        other_user = msj.idAnimalLoverReceptor if msj.idAnimalLoverEmisor == idUsuario else msj.idAnimalLoverEmisor
        key = f"{msj.idTrabajo}_{other_user}"
        
        if key not in chats_map:
            # Primera vez que vemos esta conversación — es el mensaje más reciente (para fecha)
            user_info, _ = gestionUsuario.buscarUsuario(other_user)
            nombre_usuario = f"{user_info.nombre} {user_info.apellido}" if user_info else "Desconocido"

            if msj.idTrabajo < 0:
                from repositorios import alberguesRepo, mascotasPerdidasRepo, adopcionesRepo

                if msj.idTrabajo <= -2000000:
                    id_animal = -msj.idTrabajo - 2000000
                    adopcion_detalle, adopcion_ok = adopcionesRepo.buscarAdopcionPorId(id_animal)
                    titulo_trabajo = (
                        adopcion_detalle.adopcion.nombre if adopcion_ok and adopcion_detalle else "Adopcion eliminada"
                    )
                elif msj.idTrabajo <= -1000000:
                    id_animal = -msj.idTrabajo - 1000000
                    perdida_detalle, perdida_ok = mascotasPerdidasRepo.buscarMascotaPerdidaPorId(id_animal)
                    titulo_trabajo = (
                        perdida_detalle.mascotaPerdida.nombre if perdida_ok and perdida_detalle else "Mascota eliminada"
                    )
                else:
                    id_alb = -msj.idTrabajo
                    alb_detalle, alb_ok = alberguesRepo.buscarAlberguePorId(id_alb)
                    titulo_trabajo = alb_detalle.albergue.nombre if alb_ok and alb_detalle else "Albergue eliminado"
            else:
                trabajo_info, _ = gestionTrabajo.obtenerTrabajo(msj.idTrabajo)
                titulo_trabajo = trabajo_info.nombre if trabajo_info else "Trabajo eliminado"

            chats_map[key] = {
                "idTrabajo": msj.idTrabajo,
                "idReceptor": other_user,
                "nombreUsuario": nombre_usuario,
                "tituloTrabajo": titulo_trabajo,
                "ultimoMensaje": None,           # Se llenará con el último msj del otro
                "fechaUltimoMensaje": msj.fechaMensaje  # Fecha del mensaje más reciente (cualquiera)
            }

        
        # Llenar el último mensaje de la otra persona (el primero que encontremos con emisor = other_user)
        if chats_map[key]["ultimoMensaje"] is None and msj.idAnimalLoverEmisor == other_user:
            chats_map[key]["ultimoMensaje"] = msj.contenido
    
    # Si nunca hubo mensaje del otro, poner un placeholder
    for chat in chats_map.values():
        if chat["ultimoMensaje"] is None:
            chat["ultimoMensaje"] = "Sin mensajes recibidos"
            
    lista_chats = list(chats_map.values())
    return lista_chats, True

def hayNuevosMensajes(idUsuario: int, ultimoIdMensaje: int) -> bool:
    """Verifica si hay mensajes nuevos enviados A este usuario con id_mensaje mayor al dado."""
    consulta = "SELECT COUNT(*) as total FROM mensajes WHERE id_animalLover_receptor = ? AND id_mensaje > ?"
    return mensajesRepo.contarMensajesNuevos(consulta, idUsuario, ultimoIdMensaje)


def eliminarMensajesPorTrabajo(idTrabajo: int) -> bool:
    return mensajesRepo.eliminarMensajesPorTrabajo(idTrabajo)
