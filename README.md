# TSP_HellDevs
Aquí se subirán los códigos que se harán en la materia de TSP.

Este repositorio contiene la plataforma que conecta a usuarios que ofrecen y buscan trabajos. El sistema se divide en dos partes principales: un **Backend** desarrollado en Go y un **Frontend** estructurado en HTML, CSS y JavaScript.

## Estructura del Proyecto

El proyecto está organizado en dos directorios principales: `backend/` y `frontend/`.

### 1. Backend (`/backend`)
El backend está construido con **Go (Golang)** y utiliza **SQLite** como motor de base de datos. Sigue una arquitectura organizada por modelos y repositorios.

- **`/backend/app/models/`**: Contiene las definiciones de las estructuras de datos (structs) que representan las entidades del sistema y mapean las tablas de la base de datos para la comunicación mediante JSON.
  - `Imagen.go`: Estructura para almacenar las imágenes relacionadas a un trabajo.
  - `Mensajes.go`: Estructura de la comunicación y chat entre usuarios.
  - `Trabajo.go`: Modelo principal que representa un trabajo o servicio publicado.
  - `Trabajos_aceptados.go`: Registro de los trabajos en los que dos partes han llegado a un acuerdo.
  - `Usuario.go`: Modelo con la información y credenciales de los usuarios registrados.

- **`/backend/app/Repository/`**: Contiene la lógica de acceso a datos. Cada archivo interactúa mediante sentencias SQL (usando `github.com/mattn/go-sqlite3`) para crear, buscar, actualizar o eliminar registros en la base de datos.
  - `ImagenSQLiteRepo.go`
  - `MensajesSQLiteRepo.go`
  - `TrabajoSQLiteRepo.go`
  - `TrabajosAceptadosSQLiteRepo.go`
  - `UsuarioSQLiteRepo.go`

- **`/backend/docs/`**: Contiene la documentación técnica inicial y los esquemas.
  - `sentencia.sql`: Archivo SQL que define la estructura inicial y creación de todas las tablas en la base de datos.

- **Configuraciones de entorno**: `Dockerfile` y `docker-compose.yml` para facilitar la contenedorización, el despliegue del servidor y la base de datos.

### 2. Frontend (`/frontend`)
El frontend proporciona la interfaz gráfica web y consume los servicios expuestos por el backend. Los archivos están divididos semánticamente:

- **`/frontend/html/`**: Las vistas y la estructura de las páginas que observa el usuario.
  - `index.html`: Página principal e inicio del sistema.
  - `servicios.html`: Tablón o explorador donde se listan todos los trabajos disponibles.
  - `publicar_trabajo.html`: Formulario que permite a los usuarios publicar un nuevo trabajo.
  - `mis_publicaciones.html`: Panel de gestión donde el usuario puede ver los trabajos que ha publicado.
  - `trabajos_aceptados.html`: Interfaz para ver el estado de los trabajos acordados con otros usuarios.
  - `chat.html`: Interfaz para enviar y recibir mensajes directos con otros usuarios.

- **`/frontend/css/`**: Contiene los archivos de estilos (hojas de estilo) para asegurar una interfaz atractiva visualmente.
  - `estilo_inicio.css`: Estilos para la landing page (`index.html`).
  - `estilo_servicios.css`: Estilos visuales del listado de trabajos en `servicios.html`.
  - `estilo_pubTra.css`: Estilos específicos para el formulario de `publicar_trabajo.html`.

- **`/frontend/js/`**: Lógica del cliente. Estos archivos otorgan dinamismo a las páginas y realizan peticiones AJAX (por lo general usando `fetch`) a la API de Go.
  - `servicios.js`: Se encarga de conectarse al backend, obtener los trabajos disponibles e inyectarlos dinámicamente en el DOM de `servicios.html`.
  - `publicarTrabajo.js`: Captura los eventos del formulario en `publicar_trabajo.html`, valida los datos (y de ser necesario, procesa imágenes) y envía un payload en formato JSON hacia el backend.

---

## Relación entre Archivos y Funcionamiento del Sistema

La dinámica y flujo de datos del proyecto funciona de la siguiente manera:

1. **Capa de Presentación (Frontend HTML y CSS)**
   El usuario ingresa al sistema (por ejemplo, navegando hacia `servicios.html`). El navegador lee el archivo HTML, renderiza la estructura de la página web e invoca al archivo CSS ligado (`estilo_servicios.css`) para darle la estética deseada.

2. **Interacción y Peticiones (Frontend JS)**
   A través del archivo JavaScript (`servicios.js`), el cliente ejecuta código asíncrono para comunicarse un "endpoint" o URL proporcionada por el servidor Backend. Pide, por ejemplo, la lista de trabajos o manda un trabajo nuevo (`publicarTrabajo.js`).

3. **Procesamiento de Negocio y Base de Datos (Backend y Repositorios)**
   El servidor en Go captura esa petición web y la procesa. 
   - Invoca una función dentro de **`backend/app/Repository/`** correspondiente a la tarea, por ejemplo `BuscarIDTrabajo()` o `GuardarTrabajo()` en `TrabajoSQLiteRepo.go`.
   - Estas funciones formulan las consultas SQL usando el archivo de la base de datos de SQLite, la cual fue creada siguiendo las tablas de `backend/docs/sentencia.sql`.

4. **Modelado y Retorno de Respuesta (Backend Models)**
   Los resultados de las consultas SQL son emparejados e inyectados a las instancias de los modelos de Go localizados en **`backend/app/models/`**. Estos "structs" facilitan su posterior traducción a formato JSON.

5. **Actualización del DOM**
   Finalmente, los archivos JSON viajan de regreso por la red hacia el Frontend (`.js`). El JavaScript procesa los datos JSON y los pinta en los bloques HTML generados dinámicamente, permitiendo al usuario ver, interactuar y completar sus tareas.
