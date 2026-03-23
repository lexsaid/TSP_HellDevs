package repositorios

import(
	"database/sql"
	"mizcuin/modelos"
	"os"
	"fmt"
	_ "github.com/mattn/go-sqlite3"
)

var dbPath string

func init(){
	dbPath = os.Getenv("DB_PATH")
}

func Guardar(consulta string, usuario modelos.Usuario) bool{
	db, err := sql.Open("sqlite3", dbPath)

	if err != nil {
		fmt.Println("Error al abrir la base de datos en usuario", err)
		return false
	}

	defer db.Close()

	_, err = db.Exec(consulta, usuario.Nombre, usuario.Apellido, usuario.Email, usuario.Telefono, usuario.Contraseña)
	if err != nil {
		fmt.Println("Error al ejecutar la consulta en usuario", err)
		return false
	}

	fmt.Println("Usuario guardado correctamente: ", consulta)
	return true
	
}

func BuscarIdUsuario(consulta string, id_usuario int) (modelos.Usuario, bool){
	db, err := sql.Open("sqlite3", dbPath)

	if err != nil {
		fmt.Println("Error al abrir la base de datos en usuario", err)
		return modelos.Usuario{}, false
	}

	defer db.Close()

	row := db.QueryRow(consulta, id_usuario)

	var idUsuario int
	var nombre string
	var apellido string
	var email string
	var telefono string
	var contraseña string

	err = row.Scan(&idUsuario, &nombre, &apellido, &email, &telefono, &contraseña)

	if err != nil {
		fmt.Println("Error al buscar el usuario en usuario", err)
		return modelos.Usuario{}, false
	}

	fmt.Println("Usuario encontrado correctamente: ", consulta)
	return modelos.Usuario{Id_usuario: idUsuario, Nombre: nombre, Apellido: apellido, Email: email, Telefono: telefono, Contraseña: contraseña}, true
}

// busco un usuario por su email para poder validar el login
func BuscarPorEmail(email string) (modelos.Usuario, bool){
	db, err := sql.Open("sqlite3", dbPath)

	if err != nil {
		fmt.Println("Error al abrir la base de datos en usuario", err)
		return modelos.Usuario{}, false
	}

	defer db.Close()

	consulta := "SELECT * FROM Usuario WHERE email = ?"
	row := db.QueryRow(consulta, email)

	var idUsuario int
	var nombre string
	var apellido string
	var emailDB string
	var telefono string
	var contraseña string

	err = row.Scan(&idUsuario, &nombre, &apellido, &emailDB, &telefono, &contraseña)

	if err != nil {
		fmt.Println("Error al buscar el usuario por email", err)
		return modelos.Usuario{}, false
	}

	return modelos.Usuario{Id_usuario: idUsuario, Nombre: nombre, Apellido: apellido, Email: emailDB, Telefono: telefono, Contraseña: contraseña}, true
}

func Actualizar(consulta string, usuario modelos.Usuario) bool{
	return Guardar(consulta, usuario)
}

func Eliminar(consulta string, usuario modelos.Usuario) bool{
	return Guardar(consulta, usuario)
}