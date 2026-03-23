package modelos

type Imagen struct {
	Id_imagen int `json:"id_imagen"`
	Id_trabajo int `json:"id_trabajo"`
	Imagen []byte `json:"imagen"`
}

type ListadoImagenes struct{
	Imagenes []Imagen `json:"imagenes"`
}