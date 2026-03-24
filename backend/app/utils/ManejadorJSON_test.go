package utils

import (
	"mizcuin/modelos"
	"testing"
)

// =============================================================================
// Pruebas Unitarias para ConvertirUsuario
// =============================================================================

// verifico que el conversor de usuario funcione correctamente con distintos escenarios
func TestConvertirUsuario(t *testing.T) {
	t.Run("flujo_normal_json_valido", func(t *testing.T) {
		// preparo un JSON valido con todos los campos de un usuario
		jsonValido := []byte(`{"id_usuario":1,"nombre":"Juan","apellido":"Perez","email":"juan@mail.com","telefono":"1234567890","contraseña":"abc123"}`)

		usuario, err := ConvertirUsuario(jsonValido)
		if err != nil {
			t.Fatalf("no esperaba error al convertir JSON valido, pero obtuve: %v", err)
		}

		// verifico cada campo del usuario deserializado
		if usuario.Id_usuario != 1 {
			t.Errorf("esperaba id_usuario=1, obtuve=%d", usuario.Id_usuario)
		}
		if usuario.Nombre != "Juan" {
			t.Errorf("esperaba nombre='Juan', obtuve='%s'", usuario.Nombre)
		}
		if usuario.Apellido != "Perez" {
			t.Errorf("esperaba apellido='Perez', obtuve='%s'", usuario.Apellido)
		}
		if usuario.Email != "juan@mail.com" {
			t.Errorf("esperaba email='juan@mail.com', obtuve='%s'", usuario.Email)
		}
		if usuario.Telefono != "1234567890" {
			t.Errorf("esperaba telefono='1234567890', obtuve='%s'", usuario.Telefono)
		}
		if usuario.Contraseña != "abc123" {
			t.Errorf("esperaba contraseña='abc123', obtuve='%s'", usuario.Contraseña)
		}
	})

	t.Run("json_malformado", func(t *testing.T) {
		// envio un JSON roto para validar que se devuelve un error
		jsonMalformado := []byte(`{nombre:"sin_comillas"}`)

		_, err := ConvertirUsuario(jsonMalformado)
		if err == nil {
			t.Errorf("esperaba un error al convertir JSON malformado, pero no se produjo")
		}
	})

	t.Run("campos_vacios_json_vacio", func(t *testing.T) {
		// envio un JSON vacio, debe devolver un struct con zero-values sin error
		jsonVacio := []byte(`{}`)

		usuario, err := ConvertirUsuario(jsonVacio)
		if err != nil {
			t.Fatalf("no esperaba error al convertir JSON vacio, pero obtuve: %v", err)
		}

		if usuario.Nombre != "" {
			t.Errorf("esperaba nombre vacio, obtuve='%s'", usuario.Nombre)
		}
		if usuario.Id_usuario != 0 {
			t.Errorf("esperaba id_usuario=0, obtuve=%d", usuario.Id_usuario)
		}
	})
}

// =============================================================================
// Pruebas Unitarias para ConvertirTrabajo
// =============================================================================

// verifico la conversion de JSON a Trabajo
func TestConvertirTrabajo(t *testing.T) {
	t.Run("flujo_normal_json_valido", func(t *testing.T) {
		jsonValido := []byte(`{"id_trabajo":1,"nombre":"Plomeria","ubicacion":"Col. Centro","fecha_publicacion":"2026-03-23","monto":500.50,"descripcion":"Reparacion de tuberias","id_usuario":1,"tipo_trabajo":"hogar","estado":"activo"}`)

		trabajo, err := ConvertirTrabajo(jsonValido)
		if err != nil {
			t.Fatalf("no esperaba error al convertir JSON valido, pero obtuve: %v", err)
		}

		if trabajo.Id_trabajo != 1 {
			t.Errorf("esperaba id_trabajo=1, obtuve=%d", trabajo.Id_trabajo)
		}
		if trabajo.Nombre != "Plomeria" {
			t.Errorf("esperaba nombre='Plomeria', obtuve='%s'", trabajo.Nombre)
		}
		if trabajo.Monto != 500.50 {
			t.Errorf("esperaba monto=500.50, obtuve=%f", trabajo.Monto)
		}
		if trabajo.Estado != "activo" {
			t.Errorf("esperaba estado='activo', obtuve='%s'", trabajo.Estado)
		}
	})

	t.Run("json_malformado", func(t *testing.T) {
		jsonMalformado := []byte(`{"monto": "no_es_numero"`)

		_, err := ConvertirTrabajo(jsonMalformado)
		if err == nil {
			t.Errorf("esperaba un error al convertir JSON malformado, pero no se produjo")
		}
	})

	t.Run("tipo_dato_incorrecto_monto_texto", func(t *testing.T) {
		// envio un string en el campo monto que deberia ser float64
		jsonIncorrecto := []byte(`{"monto":"quinientos"}`)

		_, err := ConvertirTrabajo(jsonIncorrecto)
		if err == nil {
			t.Errorf("esperaba un error al enviar texto en campo monto numerico, pero no se produjo")
		}
	})
}

// =============================================================================
// Pruebas Unitarias para ConvertirTrabajoAceptado
// =============================================================================

func TestConvertirTrabajoAceptado(t *testing.T) {
	t.Run("flujo_normal_json_valido", func(t *testing.T) {
		jsonValido := []byte(`{"id_trabajo":1,"id_usuario":2,"fecha_aceptacion":"2026-03-23","estado_trabajo":"Pendiente"}`)

		ta, err := ConvertirTrabajoAceptado(jsonValido)
		if err != nil {
			t.Fatalf("no esperaba error, pero obtuve: %v", err)
		}

		if ta.Id_trabajo != 1 {
			t.Errorf("esperaba id_trabajo=1, obtuve=%d", ta.Id_trabajo)
		}
		if ta.Estado_trabajo != "Pendiente" {
			t.Errorf("esperaba estado_trabajo='Pendiente', obtuve='%s'", ta.Estado_trabajo)
		}
	})

	t.Run("json_malformado", func(t *testing.T) {
		_, err := ConvertirTrabajoAceptado([]byte(`no_json`))
		if err == nil {
			t.Errorf("esperaba un error al convertir JSON malformado, pero no se produjo")
		}
	})
}

// =============================================================================
// Pruebas Unitarias para ConvertirMensajes
// =============================================================================

func TestConvertirMensajes(t *testing.T) {
	t.Run("flujo_normal_json_valido", func(t *testing.T) {
		jsonValido := []byte(`{"id_mensaje":1,"id_usuario_envia":1,"id_usuario_recibe":2,"id_trabajo":1,"contenido":"Hola","fecha_mensaje":"2026-03-23"}`)

		msg, err := ConvertirMensajes(jsonValido)
		if err != nil {
			t.Fatalf("no esperaba error, pero obtuve: %v", err)
		}

		if msg.Contenido != "Hola" {
			t.Errorf("esperaba contenido='Hola', obtuve='%s'", msg.Contenido)
		}
	})

	t.Run("json_malformado", func(t *testing.T) {
		_, err := ConvertirMensajes([]byte(`{invalido`))
		if err == nil {
			t.Errorf("esperaba un error, pero no se produjo")
		}
	})
}

// =============================================================================
// Pruebas Unitarias para ConvertirImagen
// =============================================================================

func TestConvertirImagen(t *testing.T) {
	t.Run("flujo_normal_json_valido", func(t *testing.T) {
		jsonValido := []byte(`{"id_imagen":1,"id_trabajo":1,"imagen":"aW1hZ2VuX2RlX3BydWViYQ=="}`)

		img, err := ConvertirImagen(jsonValido)
		if err != nil {
			t.Fatalf("no esperaba error, pero obtuve: %v", err)
		}

		if img.Id_trabajo != 1 {
			t.Errorf("esperaba id_trabajo=1, obtuve=%d", img.Id_trabajo)
		}
	})

	t.Run("json_malformado", func(t *testing.T) {
		_, err := ConvertirImagen([]byte(`no_json`))
		if err == nil {
			t.Errorf("esperaba error, pero no se produjo")
		}
	})
}

// =============================================================================
// Pruebas Unitarias para ConvertirMensajesRemitente
// =============================================================================

func TestConvertirMensajesRemitente(t *testing.T) {
	t.Run("flujo_normal_json_valido", func(t *testing.T) {
		jsonValido := []byte(`{"id_usuario":1,"id_trabajo":2}`)

		rem, err := ConvertirMensajesRemitente(jsonValido)
		if err != nil {
			t.Fatalf("no esperaba error, pero obtuve: %v", err)
		}

		if rem.Id_usuario != 1 {
			t.Errorf("esperaba id_usuario=1, obtuve=%d", rem.Id_usuario)
		}
		if rem.Id_trabajo != 2 {
			t.Errorf("esperaba id_trabajo=2, obtuve=%d", rem.Id_trabajo)
		}
	})

	t.Run("json_malformado", func(t *testing.T) {
		_, err := ConvertirMensajesRemitente([]byte(`}{`))
		if err == nil {
			t.Errorf("esperaba error, pero no se produjo")
		}
	})
}

// =============================================================================
// Pruebas Unitarias para ConvertirAnyToJSON
// =============================================================================

func TestConvertirAnyToJSON(t *testing.T) {
	t.Run("flujo_normal_struct_valido", func(t *testing.T) {
		usuario := modelos.Usuario{
			Id_usuario: 1,
			Nombre:     "Juan",
			Apellido:   "Perez",
			Email:      "juan@mail.com",
			Telefono:   "1234567890",
			Contraseña: "abc123",
		}

		jsonBytes, err := ConvertirAnyToJSON(usuario)
		if err != nil {
			t.Fatalf("no esperaba error al serializar struct, pero obtuve: %v", err)
		}

		if len(jsonBytes) == 0 {
			t.Errorf("esperaba un JSON no vacio, pero obtuve vacio")
		}
	})

	t.Run("flujo_normal_mapa", func(t *testing.T) {
		datos := map[string]string{"mensaje": "ok"}

		jsonBytes, err := ConvertirAnyToJSON(datos)
		if err != nil {
			t.Fatalf("no esperaba error, pero obtuve: %v", err)
		}

		esperado := `{"mensaje":"ok"}`
		if string(jsonBytes) != esperado {
			t.Errorf("esperaba '%s', obtuve='%s'", esperado, string(jsonBytes))
		}
	})
}

// =============================================================================
// Pruebas de Rendimiento (Benchmarks)
// =============================================================================

// benchmark de conversion JSON a Usuario bajo concurrencia
func BenchmarkConvertirUsuario(b *testing.B) {
	jsonValido := []byte(`{"id_usuario":1,"nombre":"Juan","apellido":"Perez","email":"juan@mail.com","telefono":"1234567890","contraseña":"abc123"}`)

	b.RunParallel(func(pb *testing.PB) {
		for pb.Next() {
			_, _ = ConvertirUsuario(jsonValido)
		}
	})
}

// benchmark de conversion JSON a Trabajo bajo concurrencia
func BenchmarkConvertirTrabajo(b *testing.B) {
	jsonValido := []byte(`{"id_trabajo":1,"nombre":"Plomeria","ubicacion":"Col. Centro","fecha_publicacion":"2026-03-23","monto":500.50,"descripcion":"Reparacion","id_usuario":1,"tipo_trabajo":"hogar","estado":"activo"}`)

	b.RunParallel(func(pb *testing.PB) {
		for pb.Next() {
			_, _ = ConvertirTrabajo(jsonValido)
		}
	})
}

// benchmark de conversion JSON a TrabajoAceptado bajo concurrencia
func BenchmarkConvertirTrabajoAceptado(b *testing.B) {
	jsonValido := []byte(`{"id_trabajo":1,"id_usuario":2,"fecha_aceptacion":"2026-03-23","estado_trabajo":"Pendiente"}`)

	b.RunParallel(func(pb *testing.PB) {
		for pb.Next() {
			_, _ = ConvertirTrabajoAceptado(jsonValido)
		}
	})
}

// benchmark de conversion JSON a Mensajes bajo concurrencia
func BenchmarkConvertirMensajes(b *testing.B) {
	jsonValido := []byte(`{"id_mensaje":1,"id_usuario_envia":1,"id_usuario_recibe":2,"id_trabajo":1,"contenido":"Hola","fecha_mensaje":"2026-03-23"}`)

	b.RunParallel(func(pb *testing.PB) {
		for pb.Next() {
			_, _ = ConvertirMensajes(jsonValido)
		}
	})
}

// benchmark de serialización de struct a JSON bajo concurrencia
func BenchmarkConvertirAnyToJSON(b *testing.B) {
	usuario := modelos.Usuario{
		Id_usuario: 1,
		Nombre:     "Juan",
		Apellido:   "Perez",
		Email:      "juan@mail.com",
		Telefono:   "1234567890",
		Contraseña: "abc123",
	}

	b.RunParallel(func(pb *testing.PB) {
		for pb.Next() {
			_, _ = ConvertirAnyToJSON(usuario)
		}
	})
}
