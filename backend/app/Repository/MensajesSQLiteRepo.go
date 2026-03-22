package repository

import(
	"database/sql"
	"mizcuin/models"
	"os"
	"fmt"
	_ "github.com/mattn/go-sqlite3"
)

var dbPathMensajes string

func init(){
	dbPathMensajes = os.Getenv("DB_PATH")
}

func GuardarMensaje(consulta string) bool{
	db, err := sql.Open("sqlite3", dbPathMensajes)

	if err != nil {
		fmt.Println("Error al abrir la base de datos en mensajes", err)
		return false
	}

	defer db.Close()

	_, err = db.Exec(consulta)
	if err != nil {
		fmt.Println("Error al ejecutar la consulta en mensajes", err)
		return false
	}

	fmt.Println("Mensaje guardado correctamente: ", consulta)
	return true
	
}

func BuscarMensajes(consulta string) (models.ListadoMensajes, bool){
	db, err := sql.Open("sqlite3", dbPathMensajes)

	if err != nil {
		fmt.Println("Error al abrir la base de datos en mensajes", err)
		return models.ListadoMensajes{}, false
	}

	defer db.Close()

	rows, err := db.Query(consulta)

	if err != nil {
		fmt.Println("Error al buscar el mensaje", err)
		return models.ListadoMensajes{}, false
	}

	defer rows.Close()

	var mensajes []models.Mensajes

	for rows.Next() {
		var idMensaje int
		var idUsuarioEnvia int
		var idUsuarioRecibe int
		var idTrabajo int

		err = rows.Scan(&idMensaje, &idUsuarioEnvia, &idUsuarioRecibe, &idTrabajo)

		if err != nil {
			fmt.Println("Error al buscar el mensaje", err)
			return models.ListadoMensajes{}, false
		}

		mensajes = append(mensajes, models.Mensajes{Id_mensaje: idMensaje, Id_usuario_envia: idUsuarioEnvia, Id_usuario_recibe: idUsuarioRecibe, Id_trabajo: idTrabajo})
	}

	fmt.Println("Mensaje encontrado correctamente: ", consulta)
	return models.ListadoMensajes{Mensajes: mensajes}, true
}

func ActualizarMensaje(consulta string) bool{
	return GuardarMensaje(consulta)
}

func EliminarMensaje(consulta string) bool{
	return GuardarMensaje(consulta)
}
