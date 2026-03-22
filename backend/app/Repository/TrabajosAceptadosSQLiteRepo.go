package repository

import(
	"database/sql"
	"mizcuin/models"
	"os"
	"fmt"
	_ "github.com/mattn/go-sqlite3"
)

var dbPathTrabajosAceptados string

func init(){
	dbPathTrabajosAceptados = os.Getenv("DB_PATH")
}

func GuardarTrabajoAceptado(consulta string) bool{
	db, err := sql.Open("sqlite3", dbPathTrabajosAceptados)

	if err != nil {
		fmt.Println("Error al abrir la base de datos en trabajos aceptados", err)
		return false
	}

	defer db.Close()

	_, err = db.Exec(consulta)
	if err != nil {
		fmt.Println("Error al ejecutar la consulta en trabajos aceptados", err)
		return false
	}

	fmt.Println("Trabajo aceptado guardado correctamente: ", consulta)
	return true
	
}

func BuscarIDTrabajoAceptado(consulta string) (models.Trabajo_aceptado, bool){
	db, err := sql.Open("sqlite3", dbPathTrabajosAceptados)

	if err != nil {
		fmt.Println("Error al abrir la base de datos en trabajos aceptados", err)
		return models.Trabajo_aceptado{}, false
	}

	defer db.Close()

	row := db.QueryRow(consulta)

	var idTrabajo int
	var idUsuario int
	var fechaAceptacion string
	var estadoTrabajo string

	err = row.Scan(&idTrabajo, &idUsuario, &fechaAceptacion, &estadoTrabajo)

	if err != nil {
		fmt.Println("Error al buscar el trabajo aceptado", err)
		return models.Trabajo_aceptado{}, false
	}

	fmt.Println("Trabajo aceptado encontrado correctamente: ", consulta)
	return models.Trabajo_aceptado{Id_trabajo: idTrabajo, Id_usuario: idUsuario, Fecha_aceptacion: fechaAceptacion, Estado_trabajo: estadoTrabajo}, true
}

func ActualizarTrabajoAceptado(consulta string) bool{
	return GuardarTrabajoAceptado(consulta)
}

func EliminarTrabajoAceptado(consulta string) bool{
	return GuardarTrabajoAceptado(consulta)
}
