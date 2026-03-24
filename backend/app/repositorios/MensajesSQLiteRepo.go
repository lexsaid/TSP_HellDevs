package repositorios

import(
	"database/sql"
	"mizcuin/modelos"
	"os"
	"fmt"
	_ "github.com/mattn/go-sqlite3"
)

var dbPathMensajes string

func init(){
	dbPathMensajes = os.Getenv("DB_PATH")
}

func GuardarMensaje(consulta string, mensaje modelos.Mensajes) bool{
	db, err := sql.Open("sqlite3", dbPathMensajes)

	if err != nil {
		fmt.Println("Error al abrir la base de datos en mensajes", err)
		return false
	}

	defer db.Close()

	_, err = db.Exec(consulta, mensaje.Id_usuario_envia, mensaje.Id_usuario_recibe, mensaje.Id_trabajo, mensaje.Contenido, mensaje.Fecha_mensaje)
	if err != nil {
		fmt.Println("Error al ejecutar la consulta en mensajes", err)
		return false
	}

	fmt.Println("Mensaje guardado correctamente: ", consulta)
	return true
	
}

func BuscarMensajes(consulta string, id_usuario int, id_trabajo int) (modelos.ListadoMensajes, bool){
	db, err := sql.Open("sqlite3", dbPathMensajes)

	if err != nil {
		fmt.Println("Error al abrir la base de datos en mensajes", err)
		return modelos.ListadoMensajes{}, false
	}

	defer db.Close()

	rows, err := db.Query(consulta, id_usuario, id_trabajo)

	if err != nil {
		fmt.Println("Error al buscar el mensaje", err)
		return modelos.ListadoMensajes{}, false
	}

	defer rows.Close()

	var mensajes []modelos.Mensajes

	for rows.Next() {
		var idMensaje int
		var idUsuarioEnvia int
		var idUsuarioRecibe int
		var idTrabajo int
		var contenido string
		var fechaMensaje string

		err = rows.Scan(&idMensaje, &idUsuarioEnvia, &idUsuarioRecibe, &idTrabajo, &contenido, &fechaMensaje)

		if err != nil {
			fmt.Println("Error al buscar el mensaje", err)
			return modelos.ListadoMensajes{}, false
		}

		mensajes = append(mensajes, modelos.Mensajes{Id_mensaje: idMensaje, Id_usuario_envia: idUsuarioEnvia, Id_usuario_recibe: idUsuarioRecibe, Id_trabajo: idTrabajo, Contenido: contenido, Fecha_mensaje: fechaMensaje})
	}

	fmt.Println("Mensaje encontrado correctamente: ", consulta)
	return modelos.ListadoMensajes{Mensajes: mensajes}, true
}

func ActualizarMensaje(consulta string, id_mensaje int, contenido string) bool{
	db, err := sql.Open("sqlite3", dbPathMensajes)

	if err != nil {
		fmt.Println("Error al abrir la base de datos en mensajes", err)
		return false
	}

	defer db.Close()

	_, err = db.Exec(consulta, id_mensaje, contenido)
	if err != nil {
		fmt.Println("Error al ejecutar la consulta en mensajes", err)
		return false
	}

	fmt.Println("Mensaje actualizado correctamente: ", consulta)
	return true
}

func EliminarMensaje(consulta string, id_mensaje int) bool{
	db, err := sql.Open("sqlite3", dbPathMensajes)

	if err != nil {
		fmt.Println("Error al abrir la base de datos en mensajes", err)
		return false
	}

	defer db.Close()

	_, err = db.Exec(consulta, id_mensaje)
	if err != nil {
		fmt.Println("Error al ejecutar la consulta en mensajes", err)
		return false
	}

	fmt.Println("Mensaje eliminado correctamente: ", consulta)
	return true
}
