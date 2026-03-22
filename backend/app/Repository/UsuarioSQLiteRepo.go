package repository

import(
	"database/sql"
	"mizcuin/models"
	"os"
	"fmt"
	_ "github.com/mattn/go-sqlite3"
)

var dbPath string

func init(){
	dbPath = os.Getenv("DB_PATH")
}

func Guardar(consulta string) bool{
	db, err := sql.Open("sqlite3", dbPath)

	if err != nil {
		fmt.Println("Error al abrir la base de datos en usuario", err)
		return false
	}

	defer db.Close()

	_, err = db.Exec(consulta)
	if err != nil {
		fmt.Println("Error al ejecutar la consulta en usuario", err)
		return false
	}

	fmt.Println("Usuario guardado correctamente: ", consulta)
	return true
	
}

func BuscarID(consulta string) (models.Usuario, bool){
	db, err := sql.Open("sqlite3", dbPath)

	if err != nil {
		fmt.Println("Error al abrir la base de datos en usuario", err)
		return models.Usuario{}, false
	}

	defer db.Close()

	row := db.QueryRow(consulta)

	var id_usuario int
	var nombre string
	var apellido string
	var email string
	var telefono string
	var contraseña string

	err = row.Scan(&id_usuario, &nombre, &apellido, &email, &telefono, &contraseña)

	if err != nil {
		fmt.Println("Error al buscar el usuario en usuario", err)
		return models.Usuario{}, false
	}

	fmt.Println("Usuario encontrado correctamente: ", consulta)
	return models.Usuario{Id_usuario: id_usuario, Nombre: nombre, Apellido: apellido, Email: email, Telefono: telefono, Contraseña: contraseña}, true
}

func Actualizar(consulta string) bool{
	return Guardar(consulta)
}

func Eliminar(consulta string) bool{
	return Guardar(consulta)
}