package manejadores

import(
	"mizcuin/modelos"
	"mizcuin/repositorios"
)

func AceptarTrabajo(trabajo modelos.Trabajo_aceptado) bool{
	consulta := "INSERT INTO Trabajo_aceptado (id_trabajo, id_usuario, fecha_aceptacion, estado_trabajo) VALUES (?, ?, ?, ?)"
	
	return repositorios.GuardarTrabajoAceptado(consulta, trabajo)
}

func ObtenerListaTrabajosAceptados(id_usuario int) (modelos.ListaTrabajosAceptados, bool){
	consulta := "SELECT * FROM Trabajo_aceptado WHERE id_usuario = ?"
	
	return repositorios.BuscarIDUsuarioTrabajo(consulta, id_usuario)
}

func ActualizarTrabajoAceptado(trabajo modelos.Trabajo_aceptado) bool{
	consulta := "UPDATE Trabajo_aceptado SET id_trabajo = ?, id_usuario = ?, fecha_aceptacion = ?, estado_trabajo = ? WHERE id_trabajo = ?"
	
	return repositorios.ActualizarTrabajoAceptado(consulta, trabajo)
}

func EliminarTrabajoAceptado(trabajo modelos.Trabajo_aceptado) bool{
	consulta := "DELETE FROM Trabajo_aceptado WHERE id_trabajo = ?"
	
	return repositorios.EliminarTrabajoAceptado(consulta, trabajo)
}