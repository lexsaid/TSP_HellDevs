package modelos

type Trabajo struct {
	Id_trabajo int `json:"id_trabajo"`
	Nombre string `json:"nombre"`
	Ubicacion string `json:"ubicacion"`
	Fecha_publicacion string `json:"fecha_publicacion"`
	Monto float64 `json:"monto"`
	Descripcion string `json:"descripcion"`
	Id_usuario int `json:"id_usuario"`
	Tipo_trabajo string `json:"tipo_trabajo"`
	Estado string `json:"estado"`
}