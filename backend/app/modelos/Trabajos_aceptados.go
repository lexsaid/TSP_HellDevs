package modelos

type Trabajo_aceptado struct {
	Id_trabajo int `json:"id_trabajo"`
	Id_usuario int `json:"id_usuario"`
	Fecha_aceptacion string `json:"fecha_aceptacion"`
	Estado_trabajo string `json:"estado_trabajo"`
}

type ListaTrabajosAceptados struct{
	ListaTrabajos []Trabajo_aceptado `json:"lista_trabajos"`
}