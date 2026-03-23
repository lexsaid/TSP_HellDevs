package modelos

type Mensajes struct {
	Id_mensaje int 
	Id_usuario_envia int 
	Id_usuario_recibe int 
	Id_trabajo int 
	Contenido string 
	Fecha_mensaje string 
}

type ListadoMensajes struct {
	Mensajes []Mensajes 
}

type MensajesRemitente struct {
	Id_usuario int `json:"id_usuario"`
	Id_trabajo int `json:"id_trabajo"`
}

type MensajeFinal struct {
	Id_mensaje int `json:"id_mensaje"`
	Remitente string `json:"remitente"`
	Id_remitente int `json:"id_remitente"`
	Receptor string `json:"receptor"`
	Id_receptor int `json:"id_receptor"`
	Id_trabajo int `json:"id_trabajo"`
	Contenido string `json:"contenido"`
	Fecha_mensaje string `json:"fecha_mensaje"`
}
	

type ListadoMensajesFinal struct {
	Mensajes []MensajeFinal `json:"mensajes"`
}
	
