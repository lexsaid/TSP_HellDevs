package modelos

type Usuario struct {
	Id_usuario int `json:"id_usuario"`
	Nombre string `json:"nombre"`
	Apellido string `json:"apellido"`
	Email string `json:"email"`
	Telefono string `json:"telefono"`
	Contraseña string `json:"contraseña"`
}

