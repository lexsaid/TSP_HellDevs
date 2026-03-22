package models

type Mensajes struct {
	Id_mensaje int `json:"id_mensaje"`
	Id_usuario_envia int `json:"id_usuario_envia"`
	Id_usuario_recibe int `json:"id_usuario_recibe"`
	Id_trabajo int `json:"id_trabajo"`
}

type ListadoMensajes struct {
	Mensajes []Mensajes `json:"mensajes"`
}