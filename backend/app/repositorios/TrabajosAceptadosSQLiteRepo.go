package repositorios

import(
	"database/sql"
	"mizcuin/modelos"
	"os"
	"fmt"
	_ "github.com/mattn/go-sqlite3"
)

var dbPathTrabajosAceptados string

func init(){
	dbPathTrabajosAceptados = os.Getenv("DB_PATH")
}

//El booleano es para indicar si la operacion se realizo correctamente
func GuardarTrabajoAceptado(consulta string, trabajo modelos.Trabajo_aceptado) bool{
	db, err := sql.Open("sqlite3", dbPathTrabajosAceptados)

	if err != nil {
		fmt.Println("Error al abrir la base de datos en trabajos aceptados", err)
		return false
	}

	defer db.Close()

	_, err = db.Exec(consulta, trabajo.Id_trabajo, trabajo.Id_usuario, trabajo.Fecha_aceptacion, trabajo.Estado_trabajo)
	if err != nil {
		fmt.Println("Error al ejecutar la consulta en trabajos aceptados", err)
		return false
	}

	fmt.Println("Trabajo aceptado guardado correctamente: ", consulta)
	return true
	
}

//Sirve para buscar la lista de todos los trabajos aceptados que se tienen registrados del usuario que se 
// indica
func BuscarIDUsuarioTrabajo(consulta string, id_usuario int) (modelos.ListaTrabajosAceptados, bool){
	db, err := sql.Open("sqlite3", dbPathTrabajosAceptados)

	if err != nil {
		fmt.Println("Error al abrir la base de datos en trabajos aceptados", err)
		return modelos.ListaTrabajosAceptados{}, false
	}

	defer db.Close()

	rows, err := db.Query(consulta, id_usuario)

	if err != nil {
		fmt.Println("Error al buscar el trabajo aceptado", err)
		return modelos.ListaTrabajosAceptados{}, false
	}

	defer rows.Close()

	listaTrabajosAceptados := modelos.ListaTrabajosAceptados{}

	for rows.Next() {
		var idTrabajo int
		var idUsuario int
		var fechaAceptacion string
		var estadoTrabajo string

	err = rows.Scan(&idTrabajo, &idUsuario, &fechaAceptacion, &estadoTrabajo)

	if err != nil {
		fmt.Println("Error al buscar el trabajo aceptado", err)
		return modelos.ListaTrabajosAceptados{}, false
	}

	fmt.Println("Trabajo aceptado encontrado correctamente: ", consulta)

	listaTrabajosAceptados.ListaTrabajos = append(listaTrabajosAceptados.ListaTrabajos, modelos.Trabajo_aceptado{Id_trabajo: idTrabajo, Id_usuario: idUsuario, Fecha_aceptacion: fechaAceptacion, Estado_trabajo: estadoTrabajo})
	}
	return listaTrabajosAceptados, true
}

func ActualizarTrabajoAceptado(consulta string, trabajo modelos.Trabajo_aceptado) bool{
	return GuardarTrabajoAceptado(consulta, trabajo)
}

func EliminarTrabajoAceptado(consulta string, trabajo modelos.Trabajo_aceptado) bool{
	return GuardarTrabajoAceptado(consulta, trabajo)
}
