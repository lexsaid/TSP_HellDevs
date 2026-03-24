package manejadores

import(
	"mizcuin/modelos"
	"mizcuin/repositorios"
)

func GuardarMensaje(mensaje modelos.Mensajes) bool{
	consulta := "INSERT INTO Mensajes (id_usuario_envia, id_usuario_recibe, id_trabajo, contenido, fecha_mensaje) VALUES (?, ?, ?, ?, ?)"
	
	return repositorios.GuardarMensaje(consulta, mensaje)
}

func ObjetenerListaMensajes(remitente modelos.MensajesRemitente) (modelos.ListadoMensajesFinal, bool){
	
	etapa1, err := obtenerMensajesRemitente(remitente.Id_usuario, remitente.Id_trabajo)

	if err == false {
		return modelos.ListadoMensajesFinal{}, false
	}

	return agruparDatosMensaje(etapa1), true
}

func obtenerMensajesRemitente(id_usuario int, id_trabajo int) (modelos.ListadoMensajes, bool){
	consulta := "SELECT * FROM Mensajes WHERE id_usuario_envia = ? AND id_trabajo = ?"
	
	return repositorios.BuscarMensajes(consulta, id_usuario, id_trabajo)
}

func agruparDatosMensaje(mensaje modelos.ListadoMensajes) modelos.ListadoMensajesFinal{
	var lista = modelos.ListadoMensajesFinal{}
	consulta := "SELECT nombre, apellido FROM Usuario WHERE id_usuario = ?"
	
	for _, idx_mensaje := range mensaje.Mensajes {
		datosUsuarioRemitente, _ := repositorios.BuscarIdUsuario(consulta, idx_mensaje.Id_usuario_envia)
		datosUsuarioReceptor, _ := repositorios.BuscarIdUsuario(consulta, idx_mensaje.Id_usuario_recibe)
		
		lista.Mensajes = append(lista.Mensajes, modelos.MensajeFinal{
			Id_mensaje: idx_mensaje.Id_mensaje,
			Remitente: datosUsuarioRemitente.Nombre + " " + datosUsuarioRemitente.Apellido,
			Id_remitente: idx_mensaje.Id_usuario_envia,
			Receptor: datosUsuarioReceptor.Nombre + " " + datosUsuarioReceptor.Apellido,
			Id_receptor: idx_mensaje.Id_usuario_recibe,
			Id_trabajo: idx_mensaje.Id_trabajo,
			Contenido: idx_mensaje.Contenido,
			Fecha_mensaje: idx_mensaje.Fecha_mensaje,
		})
	}
	
	return lista
}



func ActualizarMensaje(id_mensaje int, contenido string) bool{
	consulta := "UPDATE Mensajes SET contenido = ? WHERE id_mensaje = ?"
	
	return repositorios.ActualizarMensaje(consulta, id_mensaje, contenido)
}

func EliminarMensaje(id_mensaje int) bool{
	consulta := "DELETE FROM Mensajes WHERE id_mensaje = ?"
	
	return repositorios.EliminarMensaje(consulta, id_mensaje)
}