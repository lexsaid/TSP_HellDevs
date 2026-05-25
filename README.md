# 🐾 MIZCUIN - TSP_HellDevs

**MIZCUIN** es una plataforma web integral que conecta a usuarios para múltiples servicios relacionados con animales y mascotas:
- 💼 **Publicar y aceptar trabajos** relacionados con animales (paseos, cuidados, etc.)
- 🏠 **Albergues para animales** con capacidad y requisitos específicos
- 🐕 **Mascotas perdidas** con recompensas y búsqueda
- 💚 **Adopciones** de animales disponibles
- 💬 **Sistema de mensajería** directa entre usuarios

El sistema está dividido en un **Frontend** (HTML/CSS/JavaScript) y un **Backend** (Python con FastAPI), con arquitectura de capas y base de datos SQLite.

---

## 📂 Estructura General del Proyecto

```
TSP_HellDevs/
├── backend/                    # API y lógica de negocio (Python + FastAPI)
│   ├── app/                   # Código principal de la aplicación
│   │   ├── enrutador/         # Definición de rutas HTTP y autenticación
│   │   ├── manejadores/       # Lógica de negocio por dominio
│   │   ├── repositorios/      # Acceso a datos y queries SQL
│   │   └── modelos/           # Definiciones de estructuras de datos
│   ├── tests/                 # Suite de pruebas unitarias
│   ├── docs/                  # Documentación (esquema SQL)
│   ├── htmlcov/              # Reportes de cobertura de pruebas
│   ├── docker-compose.yml    # Orquestación de contenedores
│   └── Dockerfile            # Construcción de imagen del backend
│
└── frontend/                   # Interfaz de usuario (HTML/CSS/JavaScript)
    ├── html/                  # Archivos HTML de páginas
    ├── css/                   # Estilos CSS
    ├── js/                    # Lógica de cliente en JavaScript
    ├── nginx.conf             # Configuración del servidor web
    └── Dockerfile             # Construcción de imagen del frontend

```

---

## 🔐 Base de Datos - Diagrama de Entidades

**Ubicación**: `/backend/docs/sentencia.sql` y archivo SQLite `/app/mizcuin.db`

### Tablas principales:

```
animalLover (usuarios)
├── id_animalLover (PK)
├── nombre, apellido
├── email, telefono
├── contraseña, token

trabajo (servicios/trabajos)
├── id_trabajo (PK)
├── nombre, ubicacion, descripcion, tipo_trabajo
├── monto, fecha_publicacion
├── id_animalLover_publicador (FK → animalLover)
└── imagen (relación 1:N para fotos)

trabajo_aceptado (trabajos en proceso)
├── id_trabajo (FK → trabajo)
├── id_animalLover_trabajador (FK → animalLover)
├── fecha_aceptacion, estado_trabajo

animal (base para mascotas)
├── id_animal (PK)
├── id_animalLover (FK)
├── nombre, tamanio, color, tipo_animal, edad, etc.
├── animalPerdido (hereda de animal)
│   └── recompensa, estado
└── animalCalle (hereda de animal)
    └── vacunas, estado

albergue (refugios de animales)
├── id_albergue (PK)
├── id_animalLover (FK)
├── nombre, ubicacion, capacidad, preferencia
├── costo_diario, pre_requisitos
└── imagen_albergue (relación 1:N para fotos)

mensaje (chat entre usuarios)
├── id_mensaje (PK)
├── id_animalLover_emisor (FK)
├── id_animalLover_receptor (FK)
├── id_trabajo (FK) - contexto del mensaje
├── contenido, fecha_mensaje
```

---

## 🏗️ Backend: Arquitectura de Capas

El backend sigue un **Monolito modular** para separar responsabilidades:

### 1️⃣ **Capa de Enrutamiento** (`/backend/app/enrutador/`)

**Archivos:**
- [`enrutador.py`](backend/app/enrutador/enrutador.py) - Definición de todas las rutas HTTP
- [`AuthMiddleware.py`](backend/app/enrutador/AuthMiddleware.py) - Validación de tokens y autenticación

**Responsabilidad:**
- Registra todos los endpoints HTTP (POST, GET, PUT, DELETE)
- Actúa como punto de entrada para las solicitudes del cliente
- Middlewares CORS para permitir solicitudes desde el frontend
- Valida tokens JWT/sesión en rutas protegidas
- Parsea payloads JSON y los envía a los manejadores

**Puertos:** 
- Backend expuesto en `https://api.mizcuin.online` (producción)
- Desarrollo local: puerto `:8000` (FastAPI Uvicorn)

**Rutas principales:**
```
POST   /login                    → Autenticación
POST   /animalLover             → Registro de usuario
GET    /animalLover?id=X        → Obtener perfil
PUT    /animalLover             → Actualizar perfil
DELETE /animalLover?id=X        → Eliminar cuenta

POST   /trabajo                 → Crear trabajo
GET    /trabajo?id=X            → Ver detalle trabajo
GET    /trabajos                → Listar todos los trabajos
PUT    /trabajo                 → Editar trabajo
DELETE /trabajo?id=X            → Eliminar trabajo

POST   /trabajo/aceptar         → Aceptar un trabajo
GET    /misTrabajosAceptados    → Ver trabajos que acepté
PUT    /trabajo/estado          → Cambiar estado del trabajo

POST   /mensaje                 → Enviar mensaje
GET    /mensajes?idTrabajo=X    → Ver chat de un trabajo
GET    /chats                   → Listar todos los chats

POST   /albergue                → Crear albergue
GET    /albergue?id=X           → Ver albergue
GET    /albergues               → Listar albergues
PUT    /albergue                → Editar albergue
DELETE /albergue?id=X           → Eliminar albergue

POST   /mascotaPerdida          → Reportar mascota perdida
GET    /mascotasPerdidas        → Listar mascotas perdidas
PUT    /mascotaPerdida          → Actualizar reporte
DELETE /mascotaPerdida?id=X     → Cancelar reporte

POST   /adopcion                → Ofrecer animal en adopción
GET    /adopciones              → Listar adopciones disponibles
PUT    /adopcion                → Actualizar oferta
DELETE /adopcion?id=X           → Retirar oferta

POST   /imagen/trabajo          → Subir imagen de trabajo
GET    /imagen/trabajo?id=X     → Descargar imagen
POST   /imagen/albergue         → Subir imagen albergue
POST   /imagen/animal           → Subir imagen de animal
```

---

### 2️⃣ **Capa de Lógica de Negocio** (`/backend/app/manejadores/`)

**Archivos:**
- [`manejadorTrabajo.py`](backend/app/manejadores/manejadorTrabajo.py) - CRUD de trabajos
- [`manejadorTrabajosAceptados.py`](backend/app/manejadores/manejadorTrabajosAceptados.py) - Gestión de trabajos aceptados
- [`manejadorMensajes.py`](backend/app/manejadores/manejadorMensajes.py) - Gestión del chat
- [`manejadorUsuario.py`](backend/app/manejadores/manejadorUsuario.py) - CRUD de usuarios
- [`manejadorAlbergues.py`](backend/app/manejadores/manejadorAlbergues.py) - CRUD de albergues
- [`manejadorMasPerdidas.py`](backend/app/manejadores/manejadorMasPerdidas.py) - Mascotas perdidas
- [`manejadorAdopciones.py`](backend/app/manejadores/manejadorAdopciones.py) - Gestión de adopciones
- [`manejadorImagenes.py`](backend/app/manejadores/manejadorImagenes.py) - Procesamiento de imágenes

**Responsabilidad:**
- Implementa la lógica de negocio específica de cada dominio
- Valida reglas de negocio (ej: un usuario no puede aceptar su propio trabajo)
- Orquesta operaciones entre múltiples repositorios si es necesario
- Procesa imágenes (convierte base64 a bytes, gestiona almacenamiento)
- Maneja transacciones complejas (crear trabajo + guardar imágenes)

**Ejemplo - Crear un trabajo:**
```python
def crearTrabajo(trabajo: Trabajo) -> bool:
    # 1. Valida que el usuario exista
    # 2. Inserta el trabajo en BD vía trabajoRepo
    # 3. Si hay imágenes base64:
    #    a. Decodifica cada una
    #    b. Guarda en imagen_trabajo via imagenRepo
    # 4. Retorna éxito/fallo
```

---

### 3️⃣ **Capa de Datos** (`/backend/app/repositorios/`)

**Archivos:**
- [`database.py`](backend/app/repositorios/database.py) - Conexión a SQLite
- [`usuarioRepo.py`](backend/app/repositorios/usuarioRepo.py) - Queries de usuarios
- [`trabajoRepo.py`](backend/app/repositorios/trabajoRepo.py) - Queries de trabajos
- [`trabajosAceptadosRepo.py`](backend/app/repositorios/trabajosAceptadosRepo.py) - Queries de trabajos aceptados
- [`mensajesRepo.py`](backend/app/repositorios/mensajesRepo.py) - Queries de mensajes
- [`imagenRepo.py`](backend/app/repositorios/imagenRepo.py) - Queries de imágenes
- [`alberguesRepo.py`](backend/app/repositorios/alberguesRepo.py) - Queries de albergues
- [`mascotasPerdidasRepo.py`](backend/app/repositorios/mascotasPerdidasRepo.py) - Queries de mascotas perdidas
- [`adopcionesRepo.py`](backend/app/repositorios/adopcionesRepo.py) - Queries de adopciones

**Responsabilidad:**
- Contiene **todas las queries SQL puras** (INSERT, SELECT, UPDATE, DELETE)
- Abre/cierra conexiones a SQLite
- Convierte filas de la BD a modelos Python (Pydantic)
- Maneja errores de BD y logging
- **NO debe haber lógica de negocio**, solo SQL

**Ejemplo - Guardar usuario:**
```python
def guardarUsuario(consulta: str, usuario: AnimalLover) -> bool:
    conn = getDbConnection()
    cursor = conn.cursor()
    cursor.execute(consulta, (usuario.nombre, usuario.apellido, usuario.email, ...))
    conn.commit()
    return True
```

---

### 4️⃣ **Modelos de Datos** (`/backend/app/modelos/modelos.py`)

**Responsabilidad:**
- Define estructuras Pydantic para validación automática de datos
- Contrato de datos entre cliente y servidor
- Esquema de serialización/deserialización JSON

**Modelos principales:**
```python
class AnimalLover:           # Usuario
class Trabajo:               # Trabajo/Servicio
class TrabajoAceptado:       # Trabajo en progreso
class Mensaje:               # Mensaje en chat
class Albergue:              # Refugio de animales
class AnimalPerdido:         # Mascota reportada perdida
class AnimalCalle:           # Animal en la calle
class Imagen:                # Imagen asociada
```

---

### 5️⃣ **Autenticación** (`AuthMiddleware.py`)

**Flujo:**
1. Usuario hace login con email + contraseña
2. Backend valida en BD y genera token único
3. Token se guarda en memoria del servidor y se envía al cliente
4. Cliente envía token en header `Authorization` en cada petición
5. Middleware valida el token antes de procesar rutas protegidas
6. Si token es inválido → 401 Unauthorized
7. **Reseteo diario**: Tokens se resetean cada día a las 01:00 AM (zona CDMX)

---

## 💻 Frontend: HTML/CSS/JavaScript

### Ubicación: `/frontend/`

**Estructura:**

```
frontend/
├── html/                          # Páginas HTML
│   ├── index.html                 # Página de inicio (dashboard)
│   ├── login.html                 # Pantalla de login
│   ├── register.html              # Registro de usuario
│   ├── publicar_trabajo.html      # Crear/editar trabajo
│   ├── mis_publicaciones.html     # Mis trabajos publicados
│   ├── ver_trabajo_del_otro.html  # Ver trabajo de otro usuario
│   ├── trabajos_aceptados.html    # Trabajos que acepté
│   ├── ver_trabajo_aceptado.html  # Detalle trabajo aceptado
│   ├── chat.html                  # Sistema de mensajería
│   ├── albergue.html              # Crear/ver albergues
│   ├── mis_albergues.html         # Mis albergues publicados
│   ├── mis_mascotas_perdidas.html # Mascotas que reporté perdidas
│   ├── mis_adopciones.html        # Animales que ofrezco en adopción
│   └── ...                        # Otras páginas
│
├── js/                            # Lógica de cliente (JavaScript)
│   ├── api.js                     # Función global apiFetch() + gestión de tokens
│   ├── login.js                   # Lógica de autenticación
│   ├── publicarTrabajo.js         # Crear/editar trabajo, manejo de imágenes
│   ├── misPublicaciones.js        # Listar trabajos propios
│   ├── verTrabajo.js              # Vista detalle de trabajo
│   ├── traAceptados.js            # Mis trabajos aceptados
│   ├── chat.js                    # Sistema de mensajería
│   ├── albergue.js                # Gestión de albergues
│   ├── masPerdida.js              # Mascotas perdidas
│   ├── adopciones.js              # Gestión de adopciones
│   └── ...                        # Otros scripts
│
└── css/                           # Estilos CSS
    ├── estilo_global.css          # Estilos compartidos (header, menu, etc.)
    ├── estilo_inicio.css          # Estilos de inicio
    ├── estilo_login.css           # Estilos de login/registro
    ├── estilo_pubTra.css          # Estilos de publicación de trabajo
    ├── estilo_traAceptados.css    # Estilos de trabajos aceptados
    ├── estilo_chat.css            # Estilos del chat
    ├── estilo_albergue.css        # Estilos de albergues
    ├── estilo_mascPerdida.css     # Estilos de mascotas perdidas
    ├── estilo_adopcion.css        # Estilos de adopciones
    └── ...                        # Otros estilos
```

**Tecnología:**
- HTML5 + CSS3 (sin frameworks, puro vanilla)
- Vanilla JavaScript (ES6+)
- Fetch API para llamadas HTTP
- LocalStorage para persistencia de datos (token, ID usuario)
- FontAwesome 6.0 para iconos

---

## 🔄 Flujos de Datos Detallados

### 📋 CASO 1: Publicar un Trabajo

#### Inicio en Frontend: `publicarTrabajo.html` + `publicarTrabajo.js`

```
1. Usuario rellena formulario:
   - Título, descripción, tipo de trabajo
   - Monto, ubicación
   - Imágenes (múltiples archivos)
   
2. JavaScript valida formulario (publicarTrabajo.js):
   - Título no vacío
   - Monto > 0
   - Al menos una imagen (en creación)
   
3. Convertir imágenes a Base64:
   - Lee cada archivo con FileReader
   - Genera DataURL (data:image/png;base64,...)
   - Almacena en array imagenesBase64[]
   
4. Construir payload JSON:
   {
     "nombre": "Paseo de perro",
     "ubicacion": "Centro, CDMX",
     "tipoTrabajo": "Paseo",
     "monto": 150,
     "descripcion": "Necesito pasear a mi perro...",
     "fechaPublicacion": "2026-05-24",
     "idAnimalLoverPublicador": 5,  // Obtenido de localStorage
     "imagenesBase64": ["data:image/png;base64,...", ...]
   }
   
5. Llamada HTTP (api.js → apiFetch):
   POST https://api.mizcuin.online/trabajo
   Headers: {
     "Content-Type": "application/json",
     "Authorization": "[TOKEN]"  // del localStorage
   }
   Body: JSON anterior
```

#### En Backend: Ruta a Repositorio

```
6. FastAPI recibe POST /trabajo:
   - Middleware valida token en header Authorization
   - Si inválido → 401 Unauthorized
   - Si válido → inyecta idUsuario en contexto
   
7. Handler en enrutador.py:
   - Parsea el JSON automáticamente (FastAPI + Pydantic)
   - Crea objeto Trabajo()
   - Llama: manejadorTrabajo.crearTrabajo(trabajo)
   
8. Lógica de Negocio (manejadorTrabajo.py):
   def crearTrabajo(trabajo: Trabajo) -> bool:
       # Valida reglas de negocio
       consulta = "INSERT INTO trabajo (...) VALUES (...)"
       id_trabajo = trabajoRepo.guardarTrabajo(consulta, trabajo)
       
       if id_trabajo > 0:
           # Para cada imagen en base64:
           for img_b64 in trabajo.imagenesBase64:
               img_bytes = base64.b64decode(img_b64)
               imagen = Imagen(idTrabajo=id_trabajo, imagen=img_bytes)
               consulta_img = "INSERT INTO imagen (...) VALUES (...)"
               imagenRepo.guardarImagen(consulta_img, imagen)
       return True
   
9. Capa de Datos (repositorios):
   
   trabajoRepo.guardarTrabajo():
       conn = getDbConnection()  # Abre conexión SQLite
       cursor.execute(
           "INSERT INTO trabajo (nombre, ubicacion, ...) VALUES (?, ?, ...)",
           (trabajo.nombre, trabajo.ubicacion, ...)
       )
       conn.commit()
       return cursor.lastrowid  # ID del trabajo creado
   
   imagenRepo.guardarImagen():
       cursor.execute(
           "INSERT INTO imagen (id_trabajo, imagen) VALUES (?, ?)",
           (id_trabajo, imagen_bytes)
       )
       conn.commit()
   
10. Base de Datos (SQLite mizcuin.db):
    
    INSERT INTO trabajo VALUES (
        NULL,                          -- id_trabajo AUTO
        'Paseo de perro',
        'Centro, CDMX',
        '2026-05-24 10:30:00',
        150.0,
        'Necesito pasear a mi perro...',
        5,                             -- id_animalLover_publicador
        'Paseo'
    );
    -- Retorna: id_trabajo = 42
    
    INSERT INTO imagen VALUES (
        NULL,                          -- id_imagen AUTO
        42,                            -- id_trabajo
        [BYTES DE IMAGEN PNG],
        NULL
    );
    -- Retorna: id_imagen = 125
```

#### Respuesta al Frontend

```
11. Manejador retorna bool True
    
12. Handler HTTP convierte a JSON:
    {
        "status": "success",
        "idTrabajo": 42,
        "mensaje": "Trabajo publicado correctamente"
    }
    
13. Response HTTP (201 Created):
    Status: 201
    Headers: Content-Type: application/json
    Body: {...}
    
14. JavaScript recibe respuesta:
    - if (response.ok) → Muestra mensaje de éxito
    - Redirige a /html/mis_publicaciones.html
    - LocalStorage se actualiza con nuevo trabajo en caché (opcional)
    
15. Usuario ve "Trabajo publicado" y es redirigido a "Mis Trabajos"
```

---

### 👤 CASO 2: Login de Usuario

#### Inicio en Frontend: `login.html` + `login.js`

```
1. Usuario ingresa:
   - Email: usuario@example.com
   - Contraseña: ****
   
2. JavaScript valida (login.js):
   - Email formato válido
   - Contraseña no vacía
   
3. Llamada HTTP:
   POST https://api.mizcuin.online/login
   Body: {
     "email": "usuario@example.com",
     "contraseña": "miPassword123"
   }
```

#### En Backend

```
4. FastAPI recibe POST /login:
   - NO necesita autenticación (ruta pública)
   
5. Handler en enrutador.py:
   def loginHandler(animalLoverLogin: AnimalLoverLogin):
       usuarioDB, encontrado = usuarioRepo.buscarPorEmail(email)
       
       if not encontrado or usuarioDB.contrasena != animalLoverLogin.contrasena:
           raise HTTPException(401, "email o contraseña incorrectos")
       
       token = crearSesion(usuarioDB.idAnimalLover)
       
       return {
           "token": token,
           "idAnimalLover": usuarioDB.idAnimalLover,
           "nombre": f"{usuarioDB.nombre} {usuarioDB.apellido}"
       }
   
6. Middleware de autenticación (AuthMiddleware.py):
   def crearSesion(idAnimalLover: int) -> str:
       token = generar_token_unico()  # UUID o JWT
       tokens_en_memoria[token] = idAnimalLover
       return token
   
7. Repositorio busca en BD:
   SELECT * FROM animalLover WHERE email = ?
   
8. Base de Datos retorna usuario (si existe)
```

#### Respuesta y Almacenamiento

```
9. Backend responde:
   {
       "token": "abc123xyz789...",
       "idAnimalLover": 5,
       "nombre": "Juan García"
   }
   
10. JavaScript en login.js almacena en localStorage:
    localStorage.setItem('token', 'abc123xyz789...');
    localStorage.setItem('idAnimalLover', '5');
    localStorage.setItem('nombre', 'Juan García');
    
11. Redirige a /html/index.html (dashboard)
    
12. Cada petición futura incluye token:
    fetch(url, {
        headers: {
            'Authorization': localStorage.getItem('token')
        }
    });
```

---

### 💬 CASO 3: Enviar un Mensaje en Chat

#### Inicio en Frontend: `chat.html` + `chat.js`

```
1. Usuario abre chat de un trabajo (id_trabajo = 42)
   - Ve mensajes previos entre el publicador y trabajador
   
2. Usuario escribe mensaje:
   "Puedo hacer el trabajo mañana por la mañana"
   
3. Click en "Enviar":
   POST https://api.mizcuin.online/mensaje
   Headers: Authorization: [TOKEN]
   Body: {
       "idAnimalLoverEmisor": 5,        // Obtenido de localStorage
       "idAnimalLoverReceptor": 7,      // Del chat actual
       "idTrabajo": 42,
       "contenido": "Puedo hacer el trabajo mañana por la mañana",
       "fechaMensaje": "2026-05-24 15:30:00"
   }
```

#### En Backend

```
4. FastAPI valida token y procesa:
   - Middleware verifica token válido
   - Handler recibe mensaje
   
5. Manejador (manejadorMensajes.py):
   def guardarMensaje(mensaje: Mensaje) -> bool:
       consulta = "INSERT INTO mensaje (...) VALUES (...)"
       return mensajesRepo.guardarMensaje(consulta, mensaje)
   
6. Repositorio inserta en BD:
   INSERT INTO mensaje (
       id_animalLover_emisor,
       id_animalLover_receptor,
       id_trabajo,
       contenido,
       fecha_mensaje
   ) VALUES (5, 7, 42, '...', '2026-05-24 15:30:00')
   
7. Retorna éxito (200 OK)
```

#### Recepción de Mensajes

```
8. Otro usuario abre chat:
   GET https://api.mizcuin.online/mensajes?idTrabajo=42
   Headers: Authorization: [TOKEN]
   
9. Backend retorna todos los mensajes:
   [
       {
           "idMensaje": 1,
           "idAnimalLoverEmisor": 5,
           "nombre_emisor": "Juan García",
           "contenido": "¿Cuánto cuesta?",
           "fechaMensaje": "2026-05-24 14:00:00"
       },
       {
           "idMensaje": 2,
           "idAnimalLoverEmisor": 7,
           "nombre_emisor": "María López",
           "contenido": "$150 por paseo",
           "fechaMensaje": "2026-05-24 14:05:00"
       },
       {
           "idMensaje": 3,
           "idAnimalLoverEmisor": 5,
           "nombre_emisor": "Juan García",
           "contenido": "Puedo hacer el trabajo mañana...",
           "fechaMensaje": "2026-05-24 15:30:00"
       }
   ]
   
10. JavaScript renderiza el chat:
    - Mensaje recibido en lado derecho (para receptor)
    - Mensaje enviado en lado izquierdo (para emisor)
    - Timestamp formateado en CDMX
```

---

### ✅ CASO 4: Aceptar un Trabajo

#### Inicio en Frontend: `ver_trabajo_del_otro.html`

```
1. Usuario ve trabajo de otro:
   {
       "idTrabajo": 42,
       "nombre": "Paseo de perro",
       "monto": 150,
       "publicador": "Juan García"
   }
   
2. Click en botón "Aceptar trabajo"
   
3. Llamada HTTP:
   POST https://api.mizcuin.online/trabajo/aceptar
   Headers: Authorization: [TOKEN]
   Body: {
       "idTrabajo": 42,
       "idAnimalLoverTrabajador": 7,   // Usuario actual
       "fechaAceptacion": "2026-05-24 15:30:00",
       "estadoTrabajo": "Pendiente"
   }
```

#### En Backend

```
4. Manejador (manejadorTrabajosAceptados.py):
   def aceptarTrabajo(trabajo_aceptado: TrabajoAceptado) -> bool:
       # Validación: ¿el usuario que acepta es distinto del publicador?
       trabajo, _ = trabajoRepo.buscarIdTrabajo(trabajo_aceptado.idTrabajo)
       if trabajo.idAnimalLoverPublicador == trabajo_aceptado.idAnimalLoverTrabajador:
           raise Exception("No puedes aceptar tu propio trabajo")
       
       consulta = "INSERT INTO trabajo_aceptado (...) VALUES (...)"
       return trabajosAceptadosRepo.guardarTrabajoAceptado(consulta, trabajo_aceptado)
   
5. Base de Datos:
   INSERT INTO trabajo_aceptado (
       id_trabajo,
       id_animalLover_trabajador,
       fecha_aceptacion,
       estado_trabajo
   ) VALUES (42, 7, '2026-05-24 15:30:00', 'Pendiente')
   
6. Respuesta:
   {
       "status": "success",
       "mensaje": "Trabajo aceptado correctamente"
   }
```

#### En Frontend

```
7. Mensaje de éxito
   
8. Usuario es redirigido a /html/trabajos_aceptados.html
   
9. Ahora puede:
   - Ver trabajo en su lista de "Trabajos Aceptados"
   - Cambiar estado a "Terminado"
   - Chatear con el publicador
   - Ver estado del trabajo
```

---

### 🐕 CASO 5: Reportar Mascota Perdida

#### Inicio en Frontend: `mis_mascotas_perdidas.html`

```
1. Usuario hace clic "Reportar mascota perdida"
   
2. Formulario con campos:
   - Nombre mascota
   - Descripción (color, tamaño, raza, etc.)
   - Recompensa ofrecida
   - Imágenes de la mascota
   - Ubicación donde fue visto
   
3. Submit:
   POST https://api.mizcuin.online/mascotaPerdida
   Headers: Authorization: [TOKEN]
   Body: {
       "idAnimalLover": 5,
       "nombre": "Firulais",
       "direccion": "Calle 5 de Febrero",
       "tamanio": "Mediano",
       "color": "Blanco y marrón",
       "discapacidad": "Ninguna",
       "tipoAnimal": "Perro",
       "edad": 3,
       "recompensa": "$500",
       "estado": "Activo",
       "imagenesBase64": [...]
   }
```

#### En Backend

```
4. Manejador (manejadorMasPerdidas.py):
   def crearMascotaPerdida(animal_perdido: AnimalPerdido) -> bool:
       # Inserta en tabla animal
       id_animal = animalRepo.guardarAnimal(animal)
       
       # Inserta en tabla animalPerdido
       consulta = "INSERT INTO animalPerdido (...) VALUES (...)"
       exito = mascotasPerdidasRepo.guardarMascotaPerdida(consulta, animal_perdido)
       
       # Guarda imágenes
       for img_b64 in animal_perdido.imagenesBase64:
           img_bytes = base64.b64decode(img_b64)
           imagenAnimalRepo.guardarImagen(id_animal, img_bytes)
       
       return exito
   
5. Base de Datos:
   INSERT INTO animal (...) VALUES (...)  -- id_animal = 101
   INSERT INTO animalPerdido (...) VALUES (101, 'Firulais', '$500', 'Activo')
   INSERT INTO imagen_animal (...) VALUES (101, [IMAGEN BYTES], NOW())
```

---

## 🐳 Despliegue - Docker

### Backend (`/backend/`)

**Dockerfile:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Instala dependencias
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copia código
COPY ./app ./app

# Expone puerto
EXPOSE 8000

# Inicia servidor
CMD ["uvicorn", "app.enrutador.enrutador:app", "--host", "0.0.0.0", "--port", "8000"]
```

**docker-compose.yml:**
```yaml
version: '3.8'
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    volumes:
      - ./backend/app:/app/app
    environment:
      - DB_PATH=/app/app/mizcuin.db
```

**Ejecución:**
```bash
docker-compose up --build
# API disponible en http://localhost:8000
# Documentación interactiva en http://localhost:8000/docs
```

---

### Frontend (`/frontend/`)

**Dockerfile:**
```dockerfile
FROM nginx:latest

COPY ./html /usr/share/nginx/html/html
COPY ./css /usr/share/nginx/html/css
COPY ./js /usr/share/nginx/html/js
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80
```

**nginx.conf:**
- Sirve archivos HTML en puerto 80
- Configura CORS (permite llamadas al backend)
- Redirecciona rutas SPA a index.html

---

## 🧪 Testing

**Ubicación:** `/backend/tests/`

**Archivos:**
- `conftest.py` - Configuración común de pytest
- `test_*.py` - Suite de pruebas por módulo

**Ejecución:**
```bash
cd backend
pytest                    # Ejecuta todos los tests
pytest -v                 # Modo verboso
pytest --cov              # Con cobertura
pytest htmlcov/           # Genera reporte HTML
```

**Cobertura:** Los reportes están en `/backend/htmlcov/`

---

## 🛠️ Flujo de Trabajo de Desarrollo

### Agregar una Nueva Funcionalidad (Ej: Reportes)

**1. Define el modelo** (`/backend/app/modelos/modelos.py`):
```python
class Reporte(BaseModel):
    idReporte: Optional[int] = None
    idTrabajo: int
    idReportador: int
    razon: str
    fecha: str
```

**2. Crea queries SQL** (nuevos archivos en `/backend/app/repositorios/`):
```python
# reporteRepo.py
def guardarReporte(consulta: str, reporte: Reporte) -> bool:
    # INSERT en BD
```

**3. Implementa lógica** (`/backend/app/manejadores/`):
```python
# manejadorReportes.py
def crearReporte(reporte: Reporte) -> bool:
    # Validaciones y orquestación
```

**4. Expone en API** (`/backend/app/enrutador/enrutador.py`):
```python
@app.post("/reporte")
def crearReporte(reporte: Reporte):
    if manejadorReportes.crearReporte(reporte):
        return {"status": "success"}
    raise HTTPException(500, "Error")
```

**5. Frontend** (`/frontend/js/` y `/frontend/html/`):
- Crea formulario HTML
- Implementa JavaScript para llamada API
- Estilos en CSS

**6. Pruebas** (`/backend/tests/`):
```python
def test_crear_reporte():
    resultado = manejadorReportes.crearReporte(reporte_test)
    assert resultado == True
```

---

## 📊 Resumen: Matriz de Archivos

| Componente | Ubicación | Propósito |
|---|---|---|
| Rutas HTTP | `backend/app/enrutador/enrutador.py` | Definir endpoints |
| Autenticación | `backend/app/enrutador/AuthMiddleware.py` | Validar tokens |
| Lógica | `backend/app/manejadores/` | Reglas de negocio |
| Queries SQL | `backend/app/repositorios/` | Acceso a BD |
| Modelos | `backend/app/modelos/modelos.py` | Validación datos |
| HTML | `frontend/html/` | Páginas de usuario |
| JavaScript | `frontend/js/` | Lógica cliente + API |
| CSS | `frontend/css/` | Estilos |
| Tests | `backend/tests/` | Pruebas unitarias |
| BD | `backend/app/mizcuin.db` | Datos SQLite |

---

## 🚀 Comandos Útiles

```bash
# Backend
cd backend
uvicorn app.enrutador.enrutador:app --reload    # Dev con auto-reload
pytest                                          # Ejecutar tests
pytest --cov=app htmlcov                        # Reporte de cobertura

# Frontend
cd frontend
# Servir localmente (necesitas Python 3+)
python -m http.server 8001

# Docker
docker-compose build                            # Construir imágenes
docker-compose up                               # Iniciar servicios
docker-compose down                             # Detener servicios
```

---

## ✉️ Contacto & Documentación

- **Documentación API**: `https://api.mizcuin.online/docs` (Swagger)
- **Esquema BD**: `/backend/docs/sentencia.sql`
- **Reportes de pruebas**: `/backend/htmlcov/index.html`
