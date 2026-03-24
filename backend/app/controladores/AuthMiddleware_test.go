package controllers

import (
	"net/http"
	"net/http/httptest"
	"testing"
)

// =============================================================================
// Pruebas Unitarias para el Middleware de Autenticación
// =============================================================================

// verifico que CrearSesion genere un token no vacio y que se pueda usar para autenticar
func TestCrearSesion(t *testing.T) {
	t.Run("crear_sesion_exitosa", func(t *testing.T) {
		// creo una sesion para el usuario con id 1
		token := CrearSesion(1)

		if token == "" {
			t.Fatalf("esperaba un token no vacio, pero obtuve vacio")
		}

		// verifico que el token tenga 64 caracteres (32 bytes en hexadecimal)
		if len(token) != 64 {
			t.Errorf("esperaba un token de 64 caracteres, obtuve=%d", len(token))
		}

		// limpio la sesion despues de la prueba
		EliminarSesion(token)
	})

	t.Run("crear_dos_sesiones_genera_tokens_distintos", func(t *testing.T) {
		token1 := CrearSesion(1)
		token2 := CrearSesion(2)

		if token1 == token2 {
			t.Errorf("esperaba tokens distintos, pero ambos son iguales: %s", token1)
		}

		EliminarSesion(token1)
		EliminarSesion(token2)
	})
}

// verifico que EliminarSesion remueva correctamente el token del mapa de sesiones
func TestEliminarSesion(t *testing.T) {
	t.Run("eliminar_sesion_existente", func(t *testing.T) {
		token := CrearSesion(1)

		// verifico que la sesion existe antes de eliminarla
		mu.Lock()
		_, existe := sesiones[token]
		mu.Unlock()

		if !existe {
			t.Fatalf("la sesion deberia existir antes de eliminarla")
		}

		EliminarSesion(token)

		// verifico que la sesion ya no existe
		mu.Lock()
		_, existeDespues := sesiones[token]
		mu.Unlock()

		if existeDespues {
			t.Errorf("la sesion deberia haberse eliminado, pero aun existe")
		}
	})

	t.Run("eliminar_sesion_inexistente_no_falla", func(t *testing.T) {
		// eliminar un token que no existe no deberia causar panico
		EliminarSesion("token_que_no_existe_12345")
	})
}

// verifico que el middleware validarSesion funcione correctamente con httptest
func TestValidarSesion(t *testing.T) {
	// creo un handler dummy que sera envuelto por el middleware
	handlerDummy := http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
		w.Write([]byte(`{"mensaje":"acceso permitido"}`))
	})

	// envuelvo el handler con el middleware de autenticacion
	handlerProtegido := validarSesion(handlerDummy)

	t.Run("sin_header_authorization_devuelve_401", func(t *testing.T) {
		// simulo una peticion sin el header Authorization
		req := httptest.NewRequest(http.MethodGet, "/ruta-protegida", nil)
		rec := httptest.NewRecorder()

		handlerProtegido(rec, req)

		if rec.Code != http.StatusUnauthorized {
			t.Errorf("esperaba codigo HTTP 401, obtuve=%d", rec.Code)
		}
	})

	t.Run("token_invalido_devuelve_401", func(t *testing.T) {
		// simulo una peticion con un token que no existe en el mapa de sesiones
		req := httptest.NewRequest(http.MethodGet, "/ruta-protegida", nil)
		req.Header.Set("Authorization", "token_falso_que_no_existe")
		rec := httptest.NewRecorder()

		handlerProtegido(rec, req)

		if rec.Code != http.StatusUnauthorized {
			t.Errorf("esperaba codigo HTTP 401, obtuve=%d", rec.Code)
		}
	})

	t.Run("token_valido_permite_acceso_y_asigna_x_usuario_id", func(t *testing.T) {
		// creo una sesion real para obtener un token valido
		token := CrearSesion(42)
		defer EliminarSesion(token)

		// creo un handler que verifica que el header X-Usuario-Id fue asignado
		handlerVerificador := http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			xUsuarioId := r.Header.Get("X-Usuario-Id")
			if xUsuarioId != "42" {
				t.Errorf("esperaba X-Usuario-Id='42', obtuve='%s'", xUsuarioId)
			}
			w.WriteHeader(http.StatusOK)
		})

		handlerConAuth := validarSesion(handlerVerificador)

		req := httptest.NewRequest(http.MethodGet, "/ruta-protegida", nil)
		req.Header.Set("Authorization", token)
		rec := httptest.NewRecorder()

		handlerConAuth(rec, req)

		if rec.Code != http.StatusOK {
			t.Errorf("esperaba codigo HTTP 200, obtuve=%d", rec.Code)
		}
	})

	t.Run("token_eliminado_ya_no_permite_acceso", func(t *testing.T) {
		// creo y luego elimino una sesion
		token := CrearSesion(10)
		EliminarSesion(token)

		req := httptest.NewRequest(http.MethodGet, "/ruta-protegida", nil)
		req.Header.Set("Authorization", token)
		rec := httptest.NewRecorder()

		handlerProtegido(rec, req)

		if rec.Code != http.StatusUnauthorized {
			t.Errorf("esperaba codigo HTTP 401 con token eliminado, obtuve=%d", rec.Code)
		}
	})
}

// =============================================================================
// Pruebas de Rendimiento (Benchmarks)
// =============================================================================

// benchmark de creacion de sesiones bajo concurrencia (valida RNF-2)
func BenchmarkCrearSesion(b *testing.B) {
	b.RunParallel(func(pb *testing.PB) {
		id := 1
		for pb.Next() {
			token := CrearSesion(id)
			EliminarSesion(token) // limpio para no acumular sesiones en memoria
			id++
		}
	})
}

// benchmark de validacion de sesiones bajo concurrencia (valida RNF-2)
func BenchmarkValidarSesion(b *testing.B) {
	// preparo un token valido para las pruebas de rendimiento
	token := CrearSesion(99)
	defer EliminarSesion(token)

	handlerDummy := http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
	})
	handlerProtegido := validarSesion(handlerDummy)

	b.RunParallel(func(pb *testing.PB) {
		for pb.Next() {
			req := httptest.NewRequest(http.MethodGet, "/test", nil)
			req.Header.Set("Authorization", token)
			rec := httptest.NewRecorder()
			handlerProtegido(rec, req)
		}
	})
}
