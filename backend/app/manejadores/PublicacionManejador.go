package manejadores

import(
	"mizcuin/modelos"
	"mizcuin/repositorios"
)

func CrearTrabajo(trabajo modelos.Trabajo) bool{
	consulta := "INSERT INTO Trabajo (nombre, ubicacion, fecha_publicacion, monto, descripcion, id_usuario, tipo_trabajo, estado) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
	
	return repositorios.GuardarTrabajo(consulta, trabajo)
}

func ObtenerTrabajo(id_trabajo int) (modelos.Trabajo, bool){
	consulta := "SELECT * FROM Trabajo WHERE id_trabajo = ?"
	
	return repositorios.BuscarIDTrabajo(consulta, id_trabajo)
}

func ActualizarTrabajo(trabajo modelos.Trabajo) bool{
	consulta := "UPDATE Trabajo SET nombre = ?, ubicacion = ?, fecha_publicacion = ?, monto = ?, descripcion = ?, id_usuario = ?, tipo_trabajo = ?, estado = ? WHERE id_trabajo = ?"
	
	return repositorios.ActualizarTrabajo(consulta, trabajo)
}

func EliminarTrabajo(trabajo modelos.Trabajo) bool{
	consulta := "DELETE FROM Trabajo WHERE id_trabajo = ?"
	
	return repositorios.EliminarTrabajo(consulta, trabajo)
}