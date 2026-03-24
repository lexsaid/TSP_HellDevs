package controllers

import (
	"fmt"
	"io"
	"net/http"
	"strconv"

	"mizcuin/manejadores"
	"mizcuin/modelos"
	"mizcuin/repositorios"
	"mizcuin/utils"
)

// arranco el servidor HTTP y registro todas las rutas
func IniciarServidor() {
	// rutas publicas (no necesitan token)
	http.HandleFunc("/login", loginHandler)
	http.HandleFunc("/usuario", usuarioHandler)

	// rutas protegidas (necesitan token en el header Authorization)
	http.HandleFunc("/trabajo", validarSesion(trabajoHandler))
	http.HandleFunc("/trabajo-aceptado", validarSesion(trabajoAceptadoHandler))
	http.HandleFunc("/mensaje", validarSesion(mensajeHandler))

	fmt.Println("Servidor iniciado en el puerto 40000")
	http.ListenAndServe(":40000", nil)
}

// respondo con JSON y el status code que me pasen
func responderJSON(w http.ResponseWriter, statusCode int, datos any) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(statusCode)

	jsonResp, err := utils.ConvertirAnyToJSON(datos)
	if err != nil {
		http.Error(w, `{"error":"error al generar respuesta"}`, http.StatusInternalServerError)
		return
	}

	w.Write(jsonResp)
}

// respondo con un mensaje de error en formato JSON
func responderError(w http.ResponseWriter, statusCode int, mensaje string) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(statusCode)
	w.Write([]byte(fmt.Sprintf(`{"error":"%s"}`, mensaje)))
}

// leo el body de la solicitud y lo devuelvo como bytes
func leerBody(r *http.Request) ([]byte, error) {
	defer r.Body.Close()
	return io.ReadAll(r.Body)
}

// ==================== LOGIN ====================

// manejo el inicio de sesion: recibo email y contraseña, valido y devuelvo un token
func loginHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		responderError(w, http.StatusMethodNotAllowed, "metodo no permitido")
		return
	}

	body, err := leerBody(r)
	if err != nil {
		responderError(w, http.StatusBadRequest, "error al leer la solicitud")
		return
	}

	// solo necesito el email y la contraseña para el login
	usuario, err := utils.ConvertirUsuario(body)
	if err != nil {
		responderError(w, http.StatusBadRequest, "JSON invalido")
		return
	}

	// busco el usuario por email en la base de datos
	usuarioDB, encontrado := repositorios.BuscarPorEmail(usuario.Email)
	if !encontrado {
		responderError(w, http.StatusUnauthorized, "email o contraseña incorrectos")
		return
	}

	// comparo la contraseña que me enviaron con la que tengo guardada
	if usuarioDB.Contraseña != usuario.Contraseña {
		responderError(w, http.StatusUnauthorized, "email o contraseña incorrectos")
		return
	}

	// genero un token y lo asocio al usuario
	token := CrearSesion(usuarioDB.Id_usuario)

	responderJSON(w, http.StatusOK, map[string]any{
		"token":      token,
		"id_usuario": usuarioDB.Id_usuario,
		"nombre":     usuarioDB.Nombre + " " + usuarioDB.Apellido,
	})
}

// ==================== USUARIOS ====================

// manejo todas las operaciones de usuario segun el metodo HTTP
func usuarioHandler(w http.ResponseWriter, r *http.Request) {
	switch r.Method {
	case http.MethodPost:
		registrarUsuario(w, r)
	case http.MethodGet:
		obtenerUsuario(w, r)
	case http.MethodPut:
		actualizarUsuario(w, r)
	case http.MethodDelete:
		eliminarUsuario(w, r)
	default:
		responderError(w, http.StatusMethodNotAllowed, "metodo no permitido")
	}
}

// registro un usuario nuevo (no necesita token)
func registrarUsuario(w http.ResponseWriter, r *http.Request) {
	body, err := leerBody(r)
	if err != nil {
		responderError(w, http.StatusBadRequest, "error al leer la solicitud")
		return
	}

	usuario, err := utils.ConvertirUsuario(body)
	if err != nil {
		responderError(w, http.StatusBadRequest, "JSON invalido")
		return
	}

	if ok := manejadores.GuardarUsuario(usuario); !ok {
		responderError(w, http.StatusInternalServerError, "no se pudo registrar el usuario")
		return
	}

	responderJSON(w, http.StatusCreated, map[string]string{"mensaje": "usuario registrado correctamente"})
}

// obtengo los datos de un usuario por su id (viene como query param)
func obtenerUsuario(w http.ResponseWriter, r *http.Request) {
	idStr := r.URL.Query().Get("id")
	if idStr == "" {
		responderError(w, http.StatusBadRequest, "falta el parametro id")
		return
	}

	id, err := strconv.Atoi(idStr)
	if err != nil {
		responderError(w, http.StatusBadRequest, "id invalido")
		return
	}

	usuario, encontrado := manejadores.BuscarUsuario(modelos.Usuario{Id_usuario: id})
	if !encontrado {
		responderError(w, http.StatusNotFound, "usuario no encontrado")
		return
	}

	// no devuelvo la contraseña en la respuesta
	usuario.Contraseña = ""
	responderJSON(w, http.StatusOK, usuario)
}

// actualizo los datos de un usuario
func actualizarUsuario(w http.ResponseWriter, r *http.Request) {
	body, err := leerBody(r)
	if err != nil {
		responderError(w, http.StatusBadRequest, "error al leer la solicitud")
		return
	}

	usuario, err := utils.ConvertirUsuario(body)
	if err != nil {
		responderError(w, http.StatusBadRequest, "JSON invalido")
		return
	}

	if ok := manejadores.ActualizarUsuario(usuario); !ok {
		responderError(w, http.StatusInternalServerError, "no se pudo actualizar el usuario")
		return
	}

	responderJSON(w, http.StatusOK, map[string]string{"mensaje": "usuario actualizado correctamente"})
}

// elimino un usuario
func eliminarUsuario(w http.ResponseWriter, r *http.Request) {
	body, err := leerBody(r)
	if err != nil {
		responderError(w, http.StatusBadRequest, "error al leer la solicitud")
		return
	}

	usuario, err := utils.ConvertirUsuario(body)
	if err != nil {
		responderError(w, http.StatusBadRequest, "JSON invalido")
		return
	}

	if ok := manejadores.EliminarUsuario(usuario); !ok {
		responderError(w, http.StatusInternalServerError, "no se pudo eliminar el usuario")
		return
	}

	responderJSON(w, http.StatusOK, map[string]string{"mensaje": "usuario eliminado correctamente"})
}

// ==================== TRABAJOS (PUBLICACIONES) ====================

// manejo todas las operaciones de trabajos segun el metodo HTTP
func trabajoHandler(w http.ResponseWriter, r *http.Request) {
	switch r.Method {
	case http.MethodPost:
		crearTrabajo(w, r)
	case http.MethodGet:
		obtenerTrabajo(w, r)
	case http.MethodPut:
		actualizarTrabajo(w, r)
	case http.MethodDelete:
		eliminarTrabajo(w, r)
	default:
		responderError(w, http.StatusMethodNotAllowed, "metodo no permitido")
	}
}

// creo un trabajo nuevo
func crearTrabajo(w http.ResponseWriter, r *http.Request) {
	body, err := leerBody(r)
	if err != nil {
		responderError(w, http.StatusBadRequest, "error al leer la solicitud")
		return
	}

	trabajo, err := utils.ConvertirTrabajo(body)
	if err != nil {
		responderError(w, http.StatusBadRequest, "JSON invalido")
		return
	}

	if ok := manejadores.CrearTrabajo(trabajo); !ok {
		responderError(w, http.StatusInternalServerError, "no se pudo crear el trabajo")
		return
	}

	responderJSON(w, http.StatusCreated, map[string]string{"mensaje": "trabajo creado correctamente"})
}

// obtengo un trabajo por su id
func obtenerTrabajo(w http.ResponseWriter, r *http.Request) {
	idStr := r.URL.Query().Get("id")
	if idStr == "" {
		responderError(w, http.StatusBadRequest, "falta el parametro id")
		return
	}

	id, err := strconv.Atoi(idStr)
	if err != nil {
		responderError(w, http.StatusBadRequest, "id invalido")
		return
	}

	trabajo, encontrado := manejadores.ObtenerTrabajo(id)
	if !encontrado {
		responderError(w, http.StatusNotFound, "trabajo no encontrado")
		return
	}

	responderJSON(w, http.StatusOK, trabajo)
}

// actualizo un trabajo existente
func actualizarTrabajo(w http.ResponseWriter, r *http.Request) {
	body, err := leerBody(r)
	if err != nil {
		responderError(w, http.StatusBadRequest, "error al leer la solicitud")
		return
	}

	trabajo, err := utils.ConvertirTrabajo(body)
	if err != nil {
		responderError(w, http.StatusBadRequest, "JSON invalido")
		return
	}

	if ok := manejadores.ActualizarTrabajo(trabajo); !ok {
		responderError(w, http.StatusInternalServerError, "no se pudo actualizar el trabajo")
		return
	}

	responderJSON(w, http.StatusOK, map[string]string{"mensaje": "trabajo actualizado correctamente"})
}

// elimino un trabajo
func eliminarTrabajo(w http.ResponseWriter, r *http.Request) {
	body, err := leerBody(r)
	if err != nil {
		responderError(w, http.StatusBadRequest, "error al leer la solicitud")
		return
	}

	trabajo, err := utils.ConvertirTrabajo(body)
	if err != nil {
		responderError(w, http.StatusBadRequest, "JSON invalido")
		return
	}

	if ok := manejadores.EliminarTrabajo(trabajo); !ok {
		responderError(w, http.StatusInternalServerError, "no se pudo eliminar el trabajo")
		return
	}

	responderJSON(w, http.StatusOK, map[string]string{"mensaje": "trabajo eliminado correctamente"})
}

// ==================== TRABAJOS ACEPTADOS ====================

// manejo todas las operaciones de trabajos aceptados segun el metodo HTTP
func trabajoAceptadoHandler(w http.ResponseWriter, r *http.Request) {
	switch r.Method {
	case http.MethodPost:
		aceptarTrabajo(w, r)
	case http.MethodGet:
		listarTrabajosAceptados(w, r)
	case http.MethodPut:
		actualizarTrabajoAceptado(w, r)
	case http.MethodDelete:
		eliminarTrabajoAceptado(w, r)
	default:
		responderError(w, http.StatusMethodNotAllowed, "metodo no permitido")
	}
}

// acepto un trabajo (lo registro en la tabla de trabajos aceptados)
func aceptarTrabajo(w http.ResponseWriter, r *http.Request) {
	body, err := leerBody(r)
	if err != nil {
		responderError(w, http.StatusBadRequest, "error al leer la solicitud")
		return
	}

	trabajo, err := utils.ConvertirTrabajoAceptado(body)
	if err != nil {
		responderError(w, http.StatusBadRequest, "JSON invalido")
		return
	}

	if ok := manejadores.AceptarTrabajo(trabajo); !ok {
		responderError(w, http.StatusInternalServerError, "no se pudo aceptar el trabajo")
		return
	}

	responderJSON(w, http.StatusCreated, map[string]string{"mensaje": "trabajo aceptado correctamente"})
}

// listo todos los trabajos aceptados de un usuario
func listarTrabajosAceptados(w http.ResponseWriter, r *http.Request) {
	idStr := r.URL.Query().Get("id_usuario")
	if idStr == "" {
		responderError(w, http.StatusBadRequest, "falta el parametro id_usuario")
		return
	}

	id, err := strconv.Atoi(idStr)
	if err != nil {
		responderError(w, http.StatusBadRequest, "id_usuario invalido")
		return
	}

	lista, encontrado := manejadores.ObtenerListaTrabajosAceptados(id)
	if !encontrado {
		responderError(w, http.StatusNotFound, "no se encontraron trabajos aceptados")
		return
	}

	responderJSON(w, http.StatusOK, lista)
}

// actualizo un trabajo aceptado
func actualizarTrabajoAceptado(w http.ResponseWriter, r *http.Request) {
	body, err := leerBody(r)
	if err != nil {
		responderError(w, http.StatusBadRequest, "error al leer la solicitud")
		return
	}

	trabajo, err := utils.ConvertirTrabajoAceptado(body)
	if err != nil {
		responderError(w, http.StatusBadRequest, "JSON invalido")
		return
	}

	if ok := manejadores.ActualizarTrabajoAceptado(trabajo); !ok {
		responderError(w, http.StatusInternalServerError, "no se pudo actualizar el trabajo aceptado")
		return
	}

	responderJSON(w, http.StatusOK, map[string]string{"mensaje": "trabajo aceptado actualizado correctamente"})
}

// elimino un trabajo aceptado
func eliminarTrabajoAceptado(w http.ResponseWriter, r *http.Request) {
	body, err := leerBody(r)
	if err != nil {
		responderError(w, http.StatusBadRequest, "error al leer la solicitud")
		return
	}

	trabajo, err := utils.ConvertirTrabajoAceptado(body)
	if err != nil {
		responderError(w, http.StatusBadRequest, "JSON invalido")
		return
	}

	if ok := manejadores.EliminarTrabajoAceptado(trabajo); !ok {
		responderError(w, http.StatusInternalServerError, "no se pudo eliminar el trabajo aceptado")
		return
	}

	responderJSON(w, http.StatusOK, map[string]string{"mensaje": "trabajo aceptado eliminado correctamente"})
}

// ==================== MENSAJES ====================

// manejo todas las operaciones de mensajes segun el metodo HTTP
func mensajeHandler(w http.ResponseWriter, r *http.Request) {
	switch r.Method {
	case http.MethodPost:
		enviarMensaje(w, r)
	case http.MethodGet:
		listarMensajes(w, r)
	case http.MethodPut:
		actualizarMensaje(w, r)
	case http.MethodDelete:
		eliminarMensaje(w, r)
	default:
		responderError(w, http.StatusMethodNotAllowed, "metodo no permitido")
	}
}

// envio un mensaje nuevo
func enviarMensaje(w http.ResponseWriter, r *http.Request) {
	body, err := leerBody(r)
	if err != nil {
		responderError(w, http.StatusBadRequest, "error al leer la solicitud")
		return
	}

	mensaje, err := utils.ConvertirMensajes(body)
	if err != nil {
		responderError(w, http.StatusBadRequest, "JSON invalido")
		return
	}

	if ok := manejadores.GuardarMensaje(mensaje); !ok {
		responderError(w, http.StatusInternalServerError, "no se pudo enviar el mensaje")
		return
	}

	responderJSON(w, http.StatusCreated, map[string]string{"mensaje": "mensaje enviado correctamente"})
}

// obtengo la lista de mensajes de un usuario en un trabajo especifico
func listarMensajes(w http.ResponseWriter, r *http.Request) {
	idUsuarioStr := r.URL.Query().Get("id_usuario")
	idTrabajoStr := r.URL.Query().Get("id_trabajo")

	if idUsuarioStr == "" || idTrabajoStr == "" {
		responderError(w, http.StatusBadRequest, "faltan los parametros id_usuario e id_trabajo")
		return
	}

	idUsuario, err := strconv.Atoi(idUsuarioStr)
	if err != nil {
		responderError(w, http.StatusBadRequest, "id_usuario invalido")
		return
	}

	idTrabajo, err := strconv.Atoi(idTrabajoStr)
	if err != nil {
		responderError(w, http.StatusBadRequest, "id_trabajo invalido")
		return
	}

	remitente := modelos.MensajesRemitente{
		Id_usuario: idUsuario,
		Id_trabajo: idTrabajo,
	}

	lista, encontrado := manejadores.ObjetenerListaMensajes(remitente)
	if !encontrado {
		responderError(w, http.StatusNotFound, "no se encontraron mensajes")
		return
	}

	responderJSON(w, http.StatusOK, lista)
}

// actualizo el contenido de un mensaje
func actualizarMensaje(w http.ResponseWriter, r *http.Request) {
	idStr := r.URL.Query().Get("id_mensaje")
	if idStr == "" {
		responderError(w, http.StatusBadRequest, "falta el parametro id_mensaje")
		return
	}

	id, err := strconv.Atoi(idStr)
	if err != nil {
		responderError(w, http.StatusBadRequest, "id_mensaje invalido")
		return
	}

	body, err := leerBody(r)
	if err != nil {
		responderError(w, http.StatusBadRequest, "error al leer la solicitud")
		return
	}

	// espero recibir un JSON con el campo "contenido"
	mensaje, err := utils.ConvertirMensajes(body)
	if err != nil {
		responderError(w, http.StatusBadRequest, "JSON invalido")
		return
	}

	if ok := manejadores.ActualizarMensaje(id, mensaje.Contenido); !ok {
		responderError(w, http.StatusInternalServerError, "no se pudo actualizar el mensaje")
		return
	}

	responderJSON(w, http.StatusOK, map[string]string{"mensaje": "mensaje actualizado correctamente"})
}

// elimino un mensaje por su id
func eliminarMensaje(w http.ResponseWriter, r *http.Request) {
	idStr := r.URL.Query().Get("id_mensaje")
	if idStr == "" {
		responderError(w, http.StatusBadRequest, "falta el parametro id_mensaje")
		return
	}

	id, err := strconv.Atoi(idStr)
	if err != nil {
		responderError(w, http.StatusBadRequest, "id_mensaje invalido")
		return
	}

	if ok := manejadores.EliminarMensaje(id); !ok {
		responderError(w, http.StatusInternalServerError, "no se pudo eliminar el mensaje")
		return
	}

	responderJSON(w, http.StatusOK, map[string]string{"mensaje": "mensaje eliminado correctamente"})
}