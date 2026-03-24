# TSP_HellDevs

Plataforma que conecta a usuarios que ofrecen y buscan trabajos. El sistema se apoya fuertemente en un **Backend** desarrollado en Go (Golang) estructurado en capas, utilizando **SQLite** como motor de base de datos.

---

## 🏗️ Arquitectura del Backend

El backend está diseñado siguiendo una arquitectura de capas bien delimitadas para separar la responsabilidad de cada componente.

- **`/backend/app/interface/`**: Contiene el punto de entrada principal de la aplicación (`main.go`), el cual simplemente inicializa el servidor.
- **`/backend/app/controladores/`**: Capa de presentación HTTP.
  - `Router.go`: Define los enrutamientos (endpoints HTTP) y contiene los *handlers* que procesan las peticiones en primera instancia.
  - `AuthMiddleware.go`: Intercepta las rutas protegidas, validando los tokens de sesión en memoria y permitiendo o denegando el acceso.
- **`/backend/app/manejadores/`**: Capa de Lógica de Negocio. Aquí reside la inteligencia del sistema. Conecta los controladores con los repositorios, orquestando las acciones necesarias para cumplir con los casos de uso (ej. `GestionUsuario.go`, `MensajesManejador.go`, etc.).
- **`/backend/app/repositorios/`**: Capa de Acceso a Datos. Interactúa directamente con la base de datos SQLite (`github.com/mattn/go-sqlite3`). Contiene las sentencias SQL puras para buscar, guardar, actualizar y eliminar (`UsuarioSQLiteRepo.go`, `TrabajoSQLiteRepo.go`, etc.).
- **`/backend/app/modelos/`**: Definición de las entidades del sistema (structs en Go) como `Usuario`, `Trabajo`, `Mensajes`. Estas estructuras sirven como el contrato de datos que viaja a lo largo de todas las capas.
- **`/backend/app/utils/`**: Funciones auxiliares genéricas. Destaca `ManejadorJSON.go`, responsable centralizado de transformar los payloads JSON crudos provenientes del cliente en structs de Go, y viceversa.

---

## 🔄 Flujo de Datos: El ciclo de vida de una solicitud

Cuando un cliente (Frontend o Consumidor API) realiza una solicitud al sistema, los datos atraviesan una serie de etapas secuenciales:

### 1. Petición del Cliente
El cliente envía una solicitud HTTP (GET, POST, PUT, DELETE) hacia un endpoint específico, típicamente alojando un payload de datos en formato JSON y un header `Authorization` si la ruta lo requiere.

### 2. Router y Middleware de Autenticación
El `Router.go` captura la solicitud en el puerto `:40000`. 
- Si la ruta es pública (como `/login` o `POST /usuario`), pasa directo al handler.
- Si es privada, es interceptada por `AuthMiddleware.go`, el cual verifica el token contra su mapa en memoria. Si el token es inválido, rechaza la solicitud (401 Unauthorized); si es válido, inyecta el `id_usuario` en la petición y permite avanzar.

### 3. Controladores (Handlers HTTP)
El Handler específico (ej. `usuarioHandler`) recibe la solicitud.
- Verifica que el Método HTTP sea el correcto (switch method).
- Lee los bytes del cuerpo de la petición (`leerBody`).

### 4. Transformación de Datos (Utils)
El controlador delega la conversión de esos bytes crudos a `ManejadorJSON.go`, el cual los decodifica e hidrata los Modelos (`structs` de Go).

### 5. Lógica de Negocio (Manejadores)
Con los objetos construidos, se invoca la función pertinente de la capa de **Manejadores** (ej. `GuardarUsuario(usuario)`). Aquí se aplicarían reglas de negocio complejas, comprobaciones adicionales o se orquestan múltiples repositorios.

### 6. Acceso a Base de Datos (Repositorios)
El Manejador delega la persistencia a la rama de **Repositorios**. Esta capa recibe el modelo de datos, forma la consulta SQL correspondientes (`INSERT`, `SELECT`, `UPDATE`) y la ejecuta contra el archivo `MIZCUIN.db` de SQLite. Retorna el éxito o fallo, y opcionalmente los datos recuperados de vuelta al manejador.

### 7. Respuesta Final
El flujo regresa en cascada: Repositorio -> Manejador -> Controlador. Finalmente, el Controlador toma la resolución, utiliza nuevamente los Utils para convertir el resultado a texto JSON, y emite la respuesta HTTP final al cliente (ej. `201 Created` o `200 OK`).

---

## 🐳 Despliegue (Docker)

El backend cuenta con contenedores listos para su puesta en marcha fácil y rápida.
- `app/Dockerfile`: Compilador multi-stage (Builder y Runtime) asegurando una imagen muy ligera y con CGO activado para el soporte nativo de SQLite.
- `docker-compose.yml`: Orquestador principal que expone los recursos mapeando el volumen de datos para que la base de datos persista ante reinicios.
