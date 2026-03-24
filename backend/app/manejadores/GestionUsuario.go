package manejadores

import(
	"mizcuin/modelos"
	"mizcuin/repositorios"
)

func GuardarUsuario(usuario modelos.Usuario) bool{
	consulta := "INSERT INTO Usuario (nombre, apellido, email, telefono, contraseña) VALUES (?, ?, ?, ?, ?)"
	
	return repositorios.Guardar(consulta, usuario)
}

func BuscarUsuario(usuario modelos.Usuario) (modelos.Usuario, bool){
	consulta := "SELECT * FROM Usuario WHERE id_usuario = ?"
	
	return repositorios.BuscarIdUsuario(consulta, usuario.Id_usuario)
}

func ActualizarUsuario(usuario modelos.Usuario) bool{
	consulta := "UPDATE Usuario SET nombre = ?, apellido = ?, email = ?, telefono = ?, contraseña = ? WHERE id_usuario = ?"
	
	return repositorios.Actualizar(consulta, usuario)
}

func EliminarUsuario(usuario modelos.Usuario) bool{
	consulta := "DELETE FROM Usuario WHERE id_usuario = ?"
	
	return repositorios.Eliminar(consulta, usuario)
}