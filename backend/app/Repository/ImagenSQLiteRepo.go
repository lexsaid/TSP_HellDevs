package repository

import(
	"database/sql"
	"mizcuin/models"
	"os"
	"fmt"
	_ "github.com/mattn/go-sqlite3"
)

var dbPathImagen string

func init(){
	dbPathImagen = os.Getenv("DB_PATH")
}

func GuardarImagen(consulta string) bool{
	db, err := sql.Open("sqlite3", dbPathImagen)

	if err != nil {
		fmt.Println("Error al abrir la base de datos en imagen", err)
		return false
	}

	defer db.Close()

	_, err = db.Exec(consulta)
	if err != nil {
		fmt.Println("Error al ejecutar la consulta en imagen", err)
		return false
	}

	fmt.Println("Imagen guardada correctamente: ", consulta)
	return true
	
}

func BuscarImagenes(consulta string) (models.ListadoImagenes, bool){
	db, err := sql.Open("sqlite3", dbPathImagen)

	if err != nil {
		fmt.Println("Error al abrir la base de datos en imagen", err)
		return models.ListadoImagenes{}, false
	}

	defer db.Close()

	rows, err := db.Query(consulta)

	if err != nil {
		fmt.Println("Error al buscar la imagen", err)
		return models.ListadoImagenes{}, false
	}

	defer rows.Close()

	var imagenes []models.Imagen

	for rows.Next() {
		var idImagen int
		var idTrabajo int
		var imagen []byte

		err = rows.Scan(&idImagen, &idTrabajo, &imagen)

		if err != nil {
			fmt.Println("Error al buscar la imagen inesperado ", err)
			return models.ListadoImagenes{}, false
		}

		imagenes = append(imagenes, models.Imagen{Id_trabajo: idTrabajo, Imagen: imagen})
	}

	fmt.Println("Imagenes encontradas correctamente: ", consulta)
	return models.ListadoImagenes{Imagenes: imagenes}, true
}

func ActualizarImagen(consulta string) bool{
	return GuardarImagen(consulta)
}

func EliminarImagen(consulta string) bool{
	return GuardarImagen(consulta)
}
