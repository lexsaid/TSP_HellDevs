package repositorios

import(
	"database/sql"
	"mizcuin/modelos"
	"os"
	"fmt"
	_ "github.com/mattn/go-sqlite3"
)

var dbPathTrabajo string

func init(){
	dbPathTrabajo = os.Getenv("DB_PATH")
}

func GuardarTrabajo(consulta string, trabajo modelos.Trabajo) bool{
	db, err := sql.Open("sqlite3", dbPathTrabajo)

	if err != nil {
		fmt.Println("Error al abrir la base de datos en trabajo", err)
		return false
	}

	defer db.Close()

	_, err = db.Exec(consulta, trabajo.Nombre, trabajo.Ubicacion, trabajo.Fecha_publicacion, trabajo.Monto, trabajo.Descripcion, trabajo.Id_usuario, trabajo.Tipo_trabajo, trabajo.Estado)
	if err != nil {
		fmt.Println("Error al ejecutar la consulta en trabajo", err)
		return false
	}

	fmt.Println("Trabajo guardado correctamente: ", consulta)
	return true
	
}

func BuscarIDTrabajo(consulta string, id_trabajo int) (modelos.Trabajo, bool){
	db, err := sql.Open("sqlite3", dbPathTrabajo)

	if err != nil {
		fmt.Println("Error al abrir la base de datos en trabajo", err)
		return modelos.Trabajo{}, false
	}

	defer db.Close()

	row := db.QueryRow(consulta, id_trabajo)

	var idTrabajo int
	var nombre string
	var ubicacion string
	var fechaPublicacion string
	var monto float64
	var descripcion string
	var idUsuario int
	var tipoTrabajo string
	var estado string

	err = row.Scan(&idTrabajo, &nombre, &ubicacion, &fechaPublicacion, &monto, &descripcion, &idUsuario, &tipoTrabajo, &estado)

	if err != nil {
		fmt.Println("Error al buscar el trabajo", err)
		return modelos.Trabajo{}, false
	}

	fmt.Println("Trabajo encontrado correctamente: ", consulta)
	return modelos.Trabajo{Id_trabajo: idTrabajo, Nombre: nombre, Ubicacion: ubicacion, Fecha_publicacion: fechaPublicacion, Monto: monto, Descripcion: descripcion, Id_usuario: idUsuario, Tipo_trabajo: tipoTrabajo, Estado: estado}, true
}

func ActualizarTrabajo(consulta string, trabajo modelos.Trabajo) bool{
	return GuardarTrabajo(consulta, trabajo)
}

func EliminarTrabajo(consulta string, trabajo modelos.Trabajo) bool{
	return GuardarTrabajo(consulta, trabajo)
}
