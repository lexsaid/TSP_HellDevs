from repositorios import mensajesSQLiterepo
from modelos.Mensajes import Mensaje
from manejadores.MensajesManejador import *
from manejadores.GestionAnimalLover import *

def guardar_mensaje(mensaje) -> bool:

    consulta = (
        "INSERT INTO Mensajes (id_usuario_envia, id_usuario_recibe, "
        "id_trabajo, contenido, fecha_mensaje) VALUES (?, ?, ?, ?, ?)"
    )
    # Llamamos a la función dentro del paquete repositorios
    return mensajesSQLiterepo.guardar_mensaje(consulta, mensaje)

def objetoTenerListaMensjas( remitente ) -> bool:
    etapa1, ok = obtenerMensajesRemitente(remitente.id_animalLover_remitente, remitente.id_trabajo)
    # 2. Verificación de éxito
    if not ok:
        # Devolvemos un valor vacío (None o lista vacía) y False
        return None, False
    # 3. Procesamos los datos y retornamos con True
    resultado_final = agruparDatosMensaje(etapa1)
    return resultado_final, True

def obtenerMensajesRemitente (id_animalLover_remitente,  id_trabajo ) :
    consulta = (
        "SELECT * FROM Mensajes WHERE id_animalLover_emisor = ? AND id_trabajo = ?"
    )
    return mensajesSQLiterepo.buscar_mensajes(consulta, id_animalLover_remitente, id_trabajo)

def agruparDatosMensaje(listado_mensajes): 
    lista = ListadoMensajesFinal() 
    
    lista.mensajes = [] 
    
    consulta = "SELECT nombre, apellido FROM Usuario WHERE id_usuario = ?"
    
    for idx_mensaje in listado_mensajes: 
        datos_emisor, _ = buscar_animal_lover(consulta, idx_mensaje.id_animalLover_emisor)
        datos_receptor, _ = buscar_animal_lover(consulta, idx_mensaje.id_animalLover_receptor)
        
        nombre_emisor = f"{datos_emisor.nombre} {datos_emisor.apellido}" if datos_emisor else "Usuario Desconocido"
        nombre_receptor = f"{datos_receptor.nombre} {datos_receptor.apellido}" if datos_receptor else "Usuario Desconocido"

        nuevo_item = MensajeFinal(
            id_mensaje=idx_mensaje.id_mensaje,
            remitente=nombre_emisor,
            id_remitente=idx_mensaje.id_animalLover_emisor,
            receptor=nombre_receptor,
            id_receptor=idx_mensaje.id_animalLover_receptor,
            id_trabajo=idx_mensaje.id_trabajo,
            contenido=idx_mensaje.contenido,
            fecha_mensaje=idx_mensaje.fecha_mensaje
        )
        
        lista.mensajes.append(nuevo_item)
        
    return lista

def actualizarMensaje(id_mensaje, contenido) -> bool:
    consulta = "UPDATE Mensajes SET contenido = ? WHERE id_mensaje = ?"
    
    return actualizar_mensaje(consulta, id_mensaje, contenido)

def eliminarMensaje(id_mensaje) -> bool:
    consulta= "DELETE FROM Mensajes WHERE id_mensaje = ?"
    
    return eliminar_mensaje(consulta, id_mensaje)