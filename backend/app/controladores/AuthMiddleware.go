package controllers

import (
	"crypto/rand"
	"encoding/hex"
	"fmt"
	"net/http"
	"sync"
)

// aqui guardo las sesiones activas: token -> id_usuario
var sesiones = make(map[string]int)
var mu sync.Mutex

// genero un token aleatorio de 32 bytes en hexadecimal para usarlo como identificador de sesion
func generarToken() string {
	bytes := make([]byte, 32)
	rand.Read(bytes)
	return hex.EncodeToString(bytes)
}

// creo una sesion nueva para el usuario y le devuelvo el token generado
func CrearSesion(id_usuario int) string {
	mu.Lock()
	defer mu.Unlock()

	token := generarToken()
	sesiones[token] = id_usuario
	return token
}

// elimino la sesion del usuario cuando cierra sesion
func EliminarSesion(token string) {
	mu.Lock()
	defer mu.Unlock()

	delete(sesiones, token)
}

// verifico que el token sea valido antes de dejar pasar la solicitud
// si es valido, agrego el id_usuario al header para que los handlers lo puedan usar
func validarSesion(solicitud http.HandlerFunc) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		token := r.Header.Get("Authorization")

		if token == "" {
			http.Error(w, `{"error":"no se envio el token de autenticacion"}`, http.StatusUnauthorized)
			return
		}

		mu.Lock()
		id_usuario, existe := sesiones[token]
		mu.Unlock()

		if !existe {
			http.Error(w, `{"error":"token invalido o sesion expirada"}`, http.StatusUnauthorized)
			return
		}

		// paso el id_usuario por el header para que el handler lo pueda leer
		r.Header.Set("X-Usuario-Id", fmt.Sprintf("%d", id_usuario))
		solicitud(w, r)
	}
}