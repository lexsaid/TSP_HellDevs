package utils

import (
	"encoding/json"
	"fmt"
	"mizcuin/modelos"
)

func ConvertirUsuario(jsonModel []byte) (modelos.Usuario, error){
	var usuario modelos.Usuario
	err := json.Unmarshal(jsonModel, &usuario)
	if err != nil {
		return modelos.Usuario{}, fmt.Errorf("error al convertir el JSON a usuario: %v", err)
	}
	return usuario, nil
}

func ConvertirTrabajo(jsonModel []byte) (modelos.Trabajo, error){
	var trabajo modelos.Trabajo
	err := json.Unmarshal(jsonModel, &trabajo)
	if err != nil {
		return modelos.Trabajo{}, fmt.Errorf("error al convertir el JSON a trabajo: %v", err)
	}
	return trabajo, nil
}

func ConvertirTrabajoAceptado(jsonModel []byte) (modelos.Trabajo_aceptado, error){
	var trabajoAceptado modelos.Trabajo_aceptado
	err := json.Unmarshal(jsonModel, &trabajoAceptado)
	if err != nil {
		return modelos.Trabajo_aceptado{}, fmt.Errorf("error al convertir el JSON a trabajo aceptado: %v", err)
	}
	return trabajoAceptado, nil
}

func ConvertirImagen(jsonModel []byte) (modelos.Imagen, error){
	var imagen modelos.Imagen
	err := json.Unmarshal(jsonModel, &imagen)
	if err != nil {
		return modelos.Imagen{}, fmt.Errorf("error al convertir el JSON a imagen: %v", err)
	}
	return imagen, nil
}

func ConvertirMensajes(jsonModel []byte) (modelos.Mensajes, error){
	var mensajes modelos.Mensajes
	err := json.Unmarshal(jsonModel, &mensajes)
	if err != nil {
		return modelos.Mensajes{}, fmt.Errorf("error al convertir el JSON a mensajes: %v", err)
	}
	return mensajes, nil
}

func ConvertirMensajesRemitente(jsonModel []byte) (modelos.MensajesRemitente, error){
	var remitente modelos.MensajesRemitente
	err := json.Unmarshal(jsonModel, &remitente)
	if err != nil {
		return modelos.MensajesRemitente{}, fmt.Errorf("error al convertir el JSON a mensajes remitente: %v", err)
	}
	return remitente, nil
}

func ConvertirAnyToJSON(modelo any) ([]byte, error){
	jsonModel, err := json.Marshal(modelo)
	if err != nil {
		return nil, fmt.Errorf("error al convertir el modelo a JSON: %v", err)
	}
	return jsonModel, nil
}