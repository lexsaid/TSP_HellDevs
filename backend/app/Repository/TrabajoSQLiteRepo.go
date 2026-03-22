package repository

import(
	"database/sql"
	"mizcuin/models"
	"os"
	"fmt"
	_ "github.com/mattn/go-sqlite3"
)

var dbPathTrabajo string

func init(){
	dbPathTrabajo = os.Getenv("DB_PATH")
}

func GuardarTrabajo(consulta string) bool{
	db, err := sql.Open("sqlite3", dbPathTrabajo)

	if err != nil {
		fmt.Println("Error al abrir la base de datos en trabajo", err)
		return false
	}

	defer db.Close()

	_, err = db.Exec(consulta)
	if err != nil {
		fmt.Println("Error al ejecutar la consulta en trabajo", err)
		return false
	}

	fmt.Println("Trabajo guardado correctamente: ", consulta)
	return true
	
}

func BuscarIDTrabajo(consulta string) (models.Trabajo, bool){
	db, err := sql.Open("sqlite3", dbPathTrabajo)

	if err != nil {
		fmt.Println("Error al abrir la base de datos en trabajo", err)
		return models.Trabajo{}, false
	}

	defer db.Close()

	row := db.QueryRow(consulta)

	var idTrabajo int
	var ubicacion string
	var fechaPublicacion string
	var monto float64
	var descripcion string
	var idUsuario int
	var tipoTrabajo string
	var estado []byte

	err = row.Scan(&idTrabajo, &ubicacion, &fechaPublicacion, &monto, &descripcion, &idUsuario, &tipoTrabajo, &estado)

	if err != nil {
		fmt.Println("Error al buscar el trabajo", err)
		return models.Trabajo{}, false
	}

	fmt.Println("Trabajo encontrado correctamente: ", consulta)
	return models.Trabajo{Id_trabajo: idTrabajo, Ubicacion: ubicacion, Fecha_publicacion: fechaPublicacion, Monto: monto, Descripcion: descripcion, Id_usuario: idUsuario, Tipo_trabajo: tipoTrabajo, Estado: estado}, true
}

func ActualizarTrabajo(consulta string) bool{
	return GuardarTrabajo(consulta)
}

func EliminarTrabajo(consulta string) bool{
	return GuardarTrabajo(consulta)
}
