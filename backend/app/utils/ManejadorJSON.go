package utils

import (
	"encoding/json"
	"fmt"
	"mizcuin/models"
)

func ConvertirUsuario(jsonModel []byte) (models.Usuario, error){
	var usuario models.Usuario
	err := json.Unmarshal(jsonModel, &usuario)
	if err != nil {
		return models.Usuario{}, fmt.Errorf("error al convertir el JSON a usuario: %v", err)
	}
	return usuario, nil
}

func ConvertirTrabajo(jsonModel []byte) (models.Trabajo, error){
	var trabajo models.Trabajo
	err := json.Unmarshal(jsonModel, &trabajo)
	if err != nil {
		return models.Trabajo{}, fmt.Errorf("error al convertir el JSON a trabajo: %v", err)
	}
	return trabajo, nil
}

func ConvertirTrabajoAceptado(jsonModel []byte) (models.Trabajo_aceptado, error){
	var trabajoAceptado models.Trabajo_aceptado
	err := json.Unmarshal(jsonModel, &trabajoAceptado)
	if err != nil {
		return models.Trabajo_aceptado{}, fmt.Errorf("error al convertir el JSON a trabajo aceptado: %v", err)
	}
	return trabajoAceptado, nil
}

func ConvertirImagen(jsonModel []byte) (models.Imagen, error){
	var imagen models.Imagen
	err := json.Unmarshal(jsonModel, &imagen)
	if err != nil {
		return models.Imagen{}, fmt.Errorf("error al convertir el JSON a imagen: %v", err)
	}
	return imagen, nil
}

func ConvertirMensajes(jsonModel []byte) (models.Mensajes, error){
	var mensajes models.Mensajes
	err := json.Unmarshal(jsonModel, &mensajes)
	if err != nil {
		return models.Mensajes{}, fmt.Errorf("error al convertir el JSON a mensajes: %v", err)
	}
	return mensajes, nil
}

func ConvertirAnyToJSON(modelo any) ([]byte, error){
	jsonModel, err := json.Marshal(modelo)
	if err != nil {
		return nil, fmt.Errorf("error al convertir el modelo a JSON: %v", err)
	}
	return jsonModel, nil
}