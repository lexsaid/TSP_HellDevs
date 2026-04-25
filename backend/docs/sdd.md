# [cite_start]1. Introducción [cite: 2]

## [cite_start]1.1 Propósito [cite: 3]
[cite_start]El propósito de este Documento de Diseño del Sistema (SDD, por sus siglas en inglés) es proporcionar una descripción técnica y arquitectónica detallada para la plataforma MIZCUIN. [cite: 51] [cite_start]Este documento traduce los requerimientos de negocio y de usuario (especificados en el documento SRS) en una estructura de software técnica, sirviendo como la guía principal y definitiva para que el equipo de desarrollo (HellDevs) construya, pruebe y despliegue el sistema. [cite: 52] [cite_start]El presente SDD detalla las decisiones arquitectónicas, los modelos de datos, la estructura de componentes y los compromisos de diseño (trade-offs) necesarios para garantizar que el sistema cumpla con los atributos de calidad exigidos, tales como rendimiento, disponibilidad y mantenibilidad. [cite: 53]

## [cite_start]1.2 Alcance [cite: 4]
[cite_start]Este documento de diseño se limita estrictamente al alcance de la Primera Iteración del ciclo de vida del producto. [cite: 55] [cite_start]Las especificaciones arquitectónicas y de componentes aquí descritas cubren exclusivamente la base de la red de servicios y la comunicación entre los usuarios (Animal Lovers), abarcando los siguientes Casos de Uso: [cite: 56]
* [cite_start]CU-01: Publicar Trabajos. [cite: 57]
* [cite_start]CU-04: Contactar publicador (Chat/Mensajes). [cite: 58]
* [cite_start]CU-07: Gestionar trabajos aceptados. [cite: 59]
* [cite_start]CU-08: Gestionar publicaciones hechas. [cite: 60]
* [cite_start]CU-15: Registrar cuenta / Iniciar sesión. [cite: 61]

[cite_start]A nivel tecnológico, el alcance del diseño abarca una arquitectura monolítica modular cliente-servidor, contemplando un Front-End web responsivo, un Back-End desarrollado en Python, almacenamiento persistente en SQLite y su respectivo empaquetado mediante contenedores Docker para su despliegue en una instancia de AWS EC2. [cite: 62] [cite_start]El diseño de módulos futuros (como la pasarela de pagos o mapas interactivos) queda excluido de este documento y será abordado en iteraciones posteriores. [cite: 63]

## [cite_start]1.3 Definiciones y Acrónimos [cite: 5]

| Acrónimo | Definición |
|---|---|
| API | [cite_start]Conjunto de reglas y endpoints que permitirán al Front-End comunicarse con la lógica de negocio del Back-End en Python. [cite: 65] |
| AWS EC2 | [cite_start]Servicio de nube que proporcionará la máquina virtual (instancia) donde se alojará el sistema en producción. [cite: 65] |
| C4 Model | [cite_start]Estándar de notación gráfica utilizado en este documento para visualizar la arquitectura del software en 4 niveles de abstracción (Contexto, Contenedores, Componentes y Código). [cite: 65] |
| Docker | [cite_start]Plataforma de contenerización que empaquetará la aplicación y sus dependencias para asegurar que funcione de manera idéntica en los entornos de desarrollo, pruebas y producción. [cite: 65] |
| Endpoint | [cite_start]URL específica expuesta por el servidor Back-End que responde a peticiones HTTP (GET, POST, etc.) para realizar una acción en el sistema. [cite: 65] |
| Nginx | [cite_start]Servidor web que actuará como proxy inverso para enrutar el tráfico de los usuarios (Animal Lovers) hacia el contenedor de la aplicación. [cite: 65] |
| Trade-off | [cite_start]Decisión de diseño en la que se acepta una limitación o desventaja técnica a cambio de obtener un beneficio mayor (ej. costo o velocidad de desarrollo). [cite: 65] |
| RNF | [cite_start]Requerimiento no funcional [cite: 65] |

## [cite_start]1.4 Control de versiones [cite: 6]

| Fecha | Autor | Que modificó | Motivo |
|---|---|---|---|
| 17/04/2026 | Lex Said | Alcance, acrónimos y referencias | [cite_start]Como se hizo cambio de lenguaje de programación se tenían que cambiar estas secciones y en alcance hacia falta un CU [cite: 67] |
| 20/04/2026 | Axel Yael Rocha Gurrola | Se agregó el caso de uso 15, Se cambió las menciones de go a python, Se modificó los diagramas de secuencia, Se agregó mapa de navegación, Se modificó el diagrama de componentes y el de Entidad Relación | [cite_start]Se detectaron errores de lógica y de congruencia con el SRS, entonces se hicieron los cambios pertinentes para alinearlo con el SRS y el entorno de implementación. [cite: 67] |

## [cite_start]1.5 Referencias [cite: 7]
[cite_start]El presente diseño arquitectónico ha sido elaborado tomando como base las restricciones, requerimientos y metodologías establecidas en los siguientes documentos normativos y del proyecto: [cite: 69]
* Especificación de Requerimientos de Software (SRS) . [cite_start]Define el "qué" debe hacer el sistema. [cite: 70]
* Entorno de Implementación . [cite_start]Establece las restricciones tecnológicas, lenguajes (Python, JS) y herramientas de hardware/software aprobadas. [cite: 71]
* Plan de Proyecto . [cite_start]Define las fechas límite, hitos (milestones) de entrega y la gestión mediante la metodología SCRUM. [cite: 72]
* Estándar IEEE 1016-2009 . [cite_start]Utilizado como marco normativo para la estructura y contenido de este documento. [cite: 73]

---

# [cite_start]2. Preocupaciones de Diseño (Design Concerns) [cite: 8]
* [cite_start]**Costo Operativo y Eficiencia de Recursos (Preocupación de Gestión y Desarrollo):** Para garantizar que el Animal Lover nunca tenga que pagar por ayudar, el diseño debe ser extremadamente ligero. [cite: 75] [cite_start]Esto asegura que la plataforma se mantenga operativa sin costos de infraestructura, permitiendo que todos los recursos de la comunidad se destinen al rescate y no al mantenimiento del servidor. [cite: 76]
* [cite_start]**Fluidez en la comunicación (Preocupación del Usuario Final ( Animal Lover )):** El módulo de chat debe ser instantáneo. [cite: 77] [cite_start]El diseño técnico garantiza que el contacto entre quien reporta un animal y quien puede ayudar ocurra en menos de 5 segundos, facilitando una red de ayuda ágil y efectiva. [cite: 78]
* [cite_start]**Tolerancia a Fallos de Red (Preocupación del Usuario Final ( Animal Lover )):** Los Animal Lovers suelen usar la app en la calle con conexiones inestables. [cite: 79] [cite_start]El diseño debe incluir "memoria local" para que, si un usuario está llenando un reporte de mascota perdida o algo parecido y se queda sin señal, su información no se borre y pueda enviarse al recuperar conexión. [cite: 80]
* [cite_start]**Mantenibilidad y Portabilidad del Código (Preocupación del Equipo de Desarrollo (HellDevs)):** Para responder rápido a las nuevas necesidades de la comunidad (como nuevas formas de donar o adoptar), un diseño desacoplado permitirá que el equipo de desarrollo implemente mejoras constantes sin interrumpir el servicio actual para los usuarios. [cite: 81]
* [cite_start]**Seguridad y Control de Acceso (Preocupación de Calidad(HellDevs) y Usuario Final ( Animal Lover )):** Para proteger la integridad de los Animal Lovers, el sistema integra validaciones en cada acción, y ningún usuario podrá interactuar sin una identidad validada, garantizando que MIZCUIN sea un espacio seguro para todos. [cite: 82]

---

# [cite_start]3. Punto de Vista de Contexto (Context Viewpoint) [cite: 9]

## [cite_start]3.1 Propósito [cite: 10]
[cite_start]El propósito de este punto de vista es definir las fronteras globales del software. [cite: 85] [cite_start]Muestra a la plataforma MIZCUIN como una "caja negra" central, ilustrando exclusivamente las entidades que interactúan directamente con ella: los Animal Lovers. [cite: 86] [cite_start]Esto permite a los desarrolladores comprender el ecosistema en el que vivirá la aplicación. [cite: 87]

## [cite_start]3.2 Elementos de Diseño [cite: 11]
[cite_start]De acuerdo con el Nivel 1 del C4 Model, los elementos que participan en este punto de vista son: [cite: 89]
* **Sistema bajo diseño (System):**
    * [cite_start]MIZCUIN: La plataforma web central que facilita el ecosistema de rescate, empleos y comunicación para la comunidad. [cite: 90, 91]
* **Personas (Actors):**
    * [cite_start]Animal Lover: Usuario final que accede a la plataforma desde un navegador móvil (Chromium v145+) para publicar trabajos, comunicarse y gestionar su historial. [cite: 92, 93]

## [cite_start]3.3 Diagrama de Contexto (Nivel 1 - C4 Model) [cite: 12]
> [cite_start]**Descripción del Diagrama de Contexto:** El diagrama sirve para visualizar las relaciones con entidades externas al sistema. [cite: 95] Muestra al usuario "Animalovers" como un actor externo que envía la acción "Usa el sistema" hacia la entidad principal "Sistema MIZCUIN". [cite_start]A su vez, el sistema central envía una flecha de vuelta hacia el actor indicando "Responde el sistema". [cite: 94] 

## [cite_start]3.4 Descripción de Interacciones (Design Relationships) [cite: 13]
* [cite_start]Animal Lover-> MIZCUIN: La interacción principal se realiza a través de peticiones HTTP/HTTPS seguras desde el navegador del cliente. [cite: 97] [cite_start]El sistema MIZCUIN valida que el Animal Lover posea una sesión activa antes de procesar envíos de formularios o mensajes de chat. [cite: 98]

---

# [cite_start]4. Punto de Vista de Composición (Composition Viewpoint) [cite: 14]

## [cite_start]4.1 Propósito [cite: 15]
[cite_start]El propósito de este punto de vista es describir cómo se estructura internamente el sistema MIZCUIN en grandes contenedores o subsistemas ejecutables. [cite: 101] [cite_start]Desglosa el sistema principal en unidades de despliegue separadas, ilustrando las responsabilidades tecnológicas de alto nivel y cómo se comunican entre sí para satisfacer los requerimientos de la primera iteración. [cite: 102]

## [cite_start]4.2 Arquitectura Seleccionada [cite: 16]
[cite_start]Para resolver las necesidades del proyecto bajo los recursos de infraestructura establecidos, se ha seleccionado una Arquitectura Monolítica Modular Cliente-Servidor . [cite: 104]
* [cite_start]**Cliente-Servidor:** Mantiene una separación física y lógica entre la capa de presentación (Front-End) que reside en el dispositivo del Animal Lover , y la capa de lógica de negocio y acceso a datos (Back-End) que reside en el servidor en la nube. [cite: 105]
* [cite_start]**Monolítica Modular:** Todo el código del Back-End operará como un único proceso ejecutable (monolito) programado en Python , pero estará dividido internamente en módulos (paquetes). [cite: 106] [cite_start]Esta decisión facilita el despliegue dentro de un solo contenedor de Docker y optimiza el consumo de recursos en AWS EC2. [cite: 107]

## [cite_start]4.3 Elementos de Diseño (Contenedores) [cite: 17]
[cite_start]De acuerdo con el Nivel 2 del C4 Model, el sistema MIZCUIN se compone de los siguientes tres contenedores principales: [cite: 109]
* **Aplicación Web (Front-End):**
    * [cite_start]Tecnología: JavaScript (ES2025+), HTML5, CSS3. [cite: 110, 111]
    * [cite_start]Responsabilidad: Renderizar las interfaces del Animal Lover(UI) responsive, capturar la interacción del "Animal Lover" y aplicar las reglas de validación básicas (ej. campos obligatorios en el formulario de publicación de trabajos). [cite: 112] [cite_start]Maneja el almacenamiento en caché local para prevenir pérdida de datos ante desconexiones. [cite: 113]
* **Servidor API (Back-End):**
    * [cite_start]Tecnología: Python (Versión 3.11+). [cite: 114, 115]
    * Responsabilidad: Funcionar como el núcleo lógico del sistema. [cite_start]Expone una serie de endpoints (API RESTful) para que la Aplicación Web los consuma. [cite: 116] [cite_start]Procesa la lógica de negocio de la Iteración 1 (publicar trabajos, guardar mensajes de chat, recuperar historial) y gestiona la validación de sesiones para proteger la integridad del sistema. [cite: 117]
* **Base de Datos (Almacenamiento Persistente):**
    * [cite_start]Tecnología: SQLite (Versión 3.40.1+). [cite: 118, 119]
    * [cite_start]Responsabilidad: Actuar como el motor de persistencia relacional embebido. [cite: 120] [cite_start]Almacena de manera estructurada los registros de los Animal Lovers, ofertas de trabajo publicadas, trabajos aceptados y los hilos de mensajes del chat interno. [cite: 121]

## [cite_start]4.4 Diagrama de Contenedores (Nivel 2 - C4 Model) [cite: 18]
> [cite_start]**Descripción del Diagrama de Contenedores:** Este diagrama describe la interacción entre contenedores del sistema MIZCUIN. [cite: 123] Muestra al usuario final "Animal Lover" comunicándose con el contenedor "Aplicación Web (Front-End)" mediante visualización e interacción a través de HTTPS, recibiendo una interfaz gráfica. A su vez, esta Aplicación Web desarrollada en JavaScript, HTML y CSS envía peticiones API en JSON a través de HTTPS hacia el "Servidor API (Back-End)" escrito en Python 3.11+, el cual procesa la lógica de negocio y regresa las respuestas al front. [cite_start]Finalmente, este servidor Back-End lee y escribe registros mediante consultas SQL nativas hacia el contenedor inferior, la "Base de Datos" SQLite 3.40.1+, que le devuelve los datos solicitados. [cite: 122]

## [cite_start]4.5 Descripción de Interacciones (Design Relationships) [cite: 19]
* [cite_start]**WebApp -> Servidor API:** La comunicación entre la capa de presentación y la capa lógica se realiza estrictamente a través de peticiones asíncronas HTTP (ej. fetch en JavaScript) enviando y recibiendo cargas útiles (payloads) en formato JSON. [cite: 125]
* [cite_start]**Servidor API -> Base de Datos:** El ejecutable compilado en Python interactúa directamente con el archivo de SQLite alojado en el sistema de archivos del servidor, utilizando consultas SQL nativas a través del controlador correspondiente en Python, logrando tiempos de lectura y escritura extremadamente rápidos al no depender de una conexión de red externa para la base de datos. [cite: 126]

---

# [cite_start]5. Punto de Vista de Estructura Lógica (Structure Viewpoint) [cite: 20]

## [cite_start]5.1 Propósito [cite: 21]
[cite_start]El propósito de este punto de vista es documentar la estructura interna del contenedor del Servidor API (Back-End en Python) . [cite: 129] [cite_start]Al desglosar este contenedor en componentes lógicos y módulos, se establecen las responsabilidades específicas de cada bloque de código. [cite: 130] [cite_start]Esto garantiza la separación de responsabilidades (Separation of Concerns) y facilita la asignación de tareas al equipo de desarrollo durante la iteración 1. [cite: 131]

## [cite_start]5.2 Elementos de Diseño (Componentes del Back-End) [cite: 22]
[cite_start]Para mantener una arquitectura limpia y modular dentro del monolito en Python, el código se estructurará utilizando el patrón de diseño de Controlador-Repositorio , agrupado por dominios de negocio. [cite: 133] [cite_start]Los componentes principales que operarán en esta iteración son: [cite: 134]
* **Enrutador Central (Router):**
    * [cite_start]Responsabilidad: Es el único componente expuesto directamente a la red. [cite: 135, 136] [cite_start]Define las rutas (endpoints HTTP) y dirige el tráfico entrante hacia la cadena de middlewares y controladores correspondientes. [cite: 137]
* **AuthMiddleware:**
    * [cite_start]Responsabilidad: Interceptar las peticiones dirigidas a rutas protegidas antes de que lleguen a la lógica de negocio. [cite: 138, 139] [cite_start]Lee los encabezados (headers) de la solicitud HTTP para validar la sesión del Animal Lover. [cite: 140] [cite_start]Si es inválida, rechaza la petición; si es válida, transfiere el control (y la petición HTTP) al Controlador respectivo. [cite: 141]
* [cite_start]**Módulo de Trabajos:** [cite: 142]
    * [cite_start]Controlador de Trabajos: Recibe la solicitud HTTP ya validada por el middleware. [cite: 143] [cite_start]Extrae los datos (JSON payload), ejecuta las reglas de negocio para los CU-01 y CU-08, y formatea la respuesta HTTP de salida. [cite: 144]
    * [cite_start]Repositorio de Trabajos: Contiene la lógica nativa en Python para ejecutar las sentencias SQL de inserción, actualización y borrado de ofertas de trabajo en SQLite. [cite: 145]
* [cite_start]**Módulo de Mensajería (Chat):** [cite: 146]
    * [cite_start]Controlador de Chat: Recibe las peticiones validadas para el envío y recuperación de mensajes (CU-04). [cite: 147]
    * [cite_start]Repositorio de Mensajes: Encargado de almacenar de forma persistente el hilo de la conversación en la base de datos. [cite: 148]
* [cite_start]**Módulo de AnimalLovers:** [cite: 149]
    * [cite_start]Controlador de AnimalLovers: Extrae la identidad del Animal Lover desde la petición validada y coordina la consulta de los trabajos que ha aceptado (CU-07). [cite: 150]
    * [cite_start]Repositorio de AnimalLovers: Ejecuta consultas SQL (JOINs) para relacionar al Animal Lover con los trabajos en los que participa. [cite: 151]

## [cite_start]5.3 Diagrama de Componentes (Nivel 3 - C4) [cite: 23]
> [cite_start]**Descripción del Diagrama de Componentes:** Este esquema permite visualizar cómo las diferentes secciones del programa van a interactuar dentro de la estructura interna del código. [cite: 153] Ilustra a la Aplicación Web (JavaScript) mandando peticiones en JSON al Enrutador Central de Python, el cual intercepta el tráfico y lo redirige al Middleware de Seguridad. Si la sesión es validada, el flujo se desvía a tres grandes bloques: Módulo de Trabajos, Módulo de Chat y Módulo de AnimalLovers. En cada módulo, un Controlador procesa las reglas del negocio de sus respectivos Casos de Uso y luego delega la persistencia a un Repositorio específico. [cite_start]Estos tres repositorios finalmente se comunican de forma directa realizando lecturas o escrituras SQL hacia la Base de Datos SQLite. [cite: 152]

## [cite_start]Descripción de Interacciones (Design Relationships) [cite: 24]
[cite_start]La ejecución lógica dentro del sistema sigue un flujo secuencial estricto y de bajo acoplamiento: [cite: 155]
1. [cite_start]**Recepción y Enrutamiento:** La Aplicación Web envía un JSON al servidor. [cite: 156] [cite_start]El Enrutador Central captura la petición HTTP entrante y determina a qué ruta pertenece (ej. /api/chat). [cite: 157]
2. [cite_start]**Barrera de Seguridad:** El Enrutador envía la petición al Middleware de Autenticación . [cite: 158] [cite_start]Si la sesión es inválida, este componente devuelve un error HTTP 401 (No autorizado) y corta el flujo. [cite: 159]
3. [cite_start]**Procesamiento de Negocio:** Si la sesión es válida, el Middleware invoca la función de continuación (next.ServeHTTP()) pasando la petición al Controlador correspondiente. [cite: 160] [cite_start]El Controlador aplica las reglas de negocio, valida los tipos de datos y parámetros. [cite: 161]
4. [cite_start]**Persistencia de Datos:** El Controlador no posee conocimiento de la base de datos; [cite: 162] [cite_start]delega esta tarea invocando los métodos de su Repositorio . [cite: 163] [cite_start]El Repositorio formatea la consulta SQL de manera segura y la ejecuta en SQLite, devolviendo el resultado en sentido inverso. [cite: 164]

## [cite_start]5.4 Diseño a Nivel de Código [cite: 25]
[cite_start]Estrategia de Implementación en Python: [cite: 166]
* [cite_start]**Modelos de Base de Datos (Entidades):** Clases que representan las tablas en SQLite . [cite: 167] [cite_start]Actúan como la interfaz entre el código Python y el almacenamiento persistente. [cite: 168]
* [cite_start]**Esquemas (Pydantic Models):** Definen la estructura de los datos que viajan por la red. [cite: 169] [cite_start]Se encargan de la validación automática de tipos y la serialización/deserialización de datos, eliminando la necesidad de gestionar manualmente formatos JSON. [cite: 170]
* **Controladores:** Manejan exclusivamente el flujo HTTP (Request/Response). [cite_start]Desempaquetan los JSON y delegan la información a los manejadores. [cite: 171]
* [cite_start]**Manejadores (Capa de Lógica):** Actúan como el cerebro del sistema. [cite: 172] [cite_start]Reciben los datos, aplican las reglas del negocio utilizando sus respectivos modelos y coordinan las llamadas a la base de datos. [cite: 173]
* [cite_start]**Sentencias:** Contienen las sentencias SQL embebidas para las operaciones CRUD (Crear, Leer, Actualizar, Eliminar) interactuando directamente con SQLite. [cite: 174]

---

# [cite_start]6. Punto de Vista de Información (Information Viewpoint) [cite: 27]

## [cite_start]6.1 Propósito [cite: 28]
[cite_start]El propósito de este punto de vista es documentar la estructura de los datos persistentes del sistema, su contenido y las estrategias de gestión. [cite: 177] [cite_start]Define el esquema lógico de la base de datos relacional que soportará las funcionalidades de la primera iteración, garantizando la integridad de la información y optimizando las consultas para cumplir con los requerimientos de eficiencia. [cite: 178]

## [cite_start]6.2 Estrategia de Almacenamiento y Gestión de Datos [cite: 29]
[cite_start]La persistencia de datos se gestionará utilizando SQLite (versión 3.40.1 o superior) como motor de base de datos relacional embebido. [cite: 180] [cite_start]Dado que el sistema operará en una instancia de capa gratuita de AWS EC2, SQLite ofrece la ventaja de almacenar toda la base de datos en un único archivo local dentro del contenedor Docker. [cite: 181] [cite_start]Para mantener la arquitectura simple y facilitar el despliegue en esta primera iteración, los archivos multimedia (fotografías) se almacenarán directamente en la base de datos utilizando el tipo de dato BLOB, centralizando toda la persistencia en un solo lugar sin depender de servicios de almacenamiento externos. [cite: 182] [cite_start]Todos los campos de texto y fechas aprovecharán la afinidad de tipo TEXT nativa de SQLite. [cite: 183]

## [cite_start]6.3 Diagrama Modelo Relacional [cite: 30]
> **Descripción del Modelo Relacional:** El diagrama modela la estructura de la base de datos y la relación entre sus entidades clave. Presenta la tabla principal "AnimalLover", conectada a "Trabajo" dado que crea o publica ofertas. A su vez, la tabla "Trabajo" se vincula a "Trabajo_Aceptado" (para asignaciones), a "Imagen_Trabajo" (para almacenar adjuntos mediante el tipo de dato BLOB) y a "Mensaje" (para relacionar el chat al trabajo). Se pueden observar las llaves primarias (PK) y foráneas (FK), junto a campos de información usando INTEGER, TEXT y REAL. [cite_start]Finalmente, existen relaciones directas desde "AnimalLover" tanto para aceptar un trabajo como para enviar y recibir mensajes. [cite: 184]

## [cite_start]6.4 Diccionario de Datos (Entidades Principales) [cite: 31]
[cite_start]Para asegurar la correcta implementación en los repositorios de Python, se establecen las siguientes definiciones de entidades (alineadas a los tipos nativos de SQLite): [cite: 186]
* **AnimalLover :** Almacena la identidad y credenciales de los Animal Lovers. [cite_start]La contraseña debe guardarse obligatoriamente como un hash criptográfico. [cite: 187] [cite_start]Las fechas se manejan como cadenas de texto (TEXT). [cite: 188]
* [cite_start]**Trabajo :** Contiene la información de las ofertas de empleo o micro-tareas creadas (CU-01). [cite: 189]
* [cite_start]**Imagen_Trabajo :** Tabla que permite asociar una o múltiples fotografías a una publicación de trabajo. [cite: 190] [cite_start]Los datos binarios crudos de la fotografía se almacenan directamente en el campo imagen mediante el tipo de dato BLOB. [cite: 191]
* [cite_start]**Trabajo_Aceptado :** Entidad asociativa (tabla pivote) que resuelve la relación muchos-a-muchos entre un Animal Lover que busca ayudar y un trabajo disponible. [cite: 192] [cite_start]Permite diferenciar qué trabajos están "Pendientes" y cuáles "Completados" (CU-07). [cite: 193]
* [cite_start]**Mensaje :** Estructura que almacena los hilos de comunicación interna del chat (CU-04). [cite: 194] [cite_start]Mantiene las llaves foráneas tanto del remitente como del receptor, así como la referencia opcional (id_trabajo_ref) para saber sobre qué publicación específica se está conversando. [cite: 195]

---

# [cite_start]7. Punto de Vista de Interacción (Interaction Viewpoint) [cite: 32]

## [cite_start]7.1 Propósito [cite: 33]
[cite_start]El propósito de este punto de vista es definir cómo colaboran los componentes del sistema de forma dinámica y en tiempo de ejecución para cumplir con un escenario o funcionalidad específica. [cite: 198] [cite_start]Mientras que las secciones anteriores describieron la estructura estática del código y los datos, esta sección detalla el flujo de mensajes, las llamadas a funciones y el paso de parámetros entre la Aplicación Web (Front-End), el Servidor API (Back-End) y la Base de Datos. [cite: 199]

## [cite_start]7.2 Estrategia de Interacción [cite: 34]
[cite_start]Todas las interacciones entre el cliente y el servidor siguen un modelo síncrono de petición-respuesta (Request-Response) basado en el protocolo HTTP/HTTPS. [cite: 201] [cite_start]El flujo respeta estrictamente la cadena de responsabilidad definida en la arquitectura: el Enrutador captura la petición , el Middleware valida la seguridad , el Controlador ejecuta las reglas de negocio y el Repositorio gestiona la persistencia. [cite: 202]

## [cite_start]7.3 Diagrama de Secuencia [cite: 35]

[cite_start]**CU-01 Publicar trabajos** [cite: 36]
> **Descripción del Diagrama CU-01:** Este diagrama secuencial muestra el flujo de trabajo para publicar una oferta. Comienza con el "Animal Lover" navegando en la WebApp por la sección "Servicios", hasta llegar al formulario de publicación. Se manejan validaciones locales, y una caché por si ocurre una pérdida de red. [cite_start]Al estar listo, la aplicación emite una petición POST al "Enrutador", pasa la validación de sesión por el "Middleware Auth", ejecuta las lógicas a través del "Controlador Publicaciones" y envía una sentencia de inserción mediante el "Repositorio Publicaciones" a "SQLite", devolviendo un código 201 Created para que la interfaz confirme la creación en pantalla. [cite: 204]

[cite_start]**CU-04 Contactar publicador** [cite: 37]
> **Descripción del Diagrama CU-04:** Enseña la secuencia de comunicación de mensajería. El trabajador entra al detalle de la publicación, escribe un mensaje en la WebApp y lo envía. La solicitud entra por el Enrutador hacia el Middleware Auth, donde en caso de sesión inválida se corta con error, pero si es correcta se sigue al Controlador Chat para aplicar las reglas de longitud o filtros. [cite_start]Posteriormente, se efectúa un INSERT INTO hacia la Base de Datos con el Repositorio Chat, propagando el éxito de vuelta al usuario para actualizar la interfaz. [cite: 205]

[cite_start]**CU-07 Gestionar trabajos aceptados** [cite: 38]
> **Descripción del Diagrama CU-07:** Ilustra las operaciones del trabajador para administrar sus participaciones. Solicita a la plataforma su historial de trabajos aceptados, navegando por las capas de la arquitectura (Enrutador, Middleware, Controlador, Repositorio) hacia la BD para obtener una lista. [cite_start]Desde ahí, el usuario tiene la opción condicional de "Dar de baja", lo que confirmaría un cambio de estado en la base de datos, o de pedir "Más información", lo que consulta un detalle completo del trabajo en SQLite para ser desempaquetado y visualizado en la interfaz web. [cite: 206]

[cite_start]**CU-08 Gestionar publicaciones hechas** [cite: 39]
> **Descripción del Diagrama CU-08:** Muestra cómo el publicador maneja su propio historial de trabajos creados. [cite_start]Tras consultar la lista con el servidor, el flujo se bifurca: puede solicitar "Dar de baja publicación", lo cual activa un proceso desde la WebApp hasta el Repositorio Publicaciones para eliminar el registro en la base de datos, o puede seleccionar "Editar publicación", lo que abre un formulario prellenado para actualizar la información, validarla en backend y guardar los cambios sobreescribiendo los registros en SQLite. [cite: 207]

[cite_start]**CU-15: Registrar cuenta / Iniciar sesión** [cite: 61]
> **Descripción del Diagrama CU-15:** Representa el proceso de autenticación. El usuario ingresa credenciales en la pestaña de login. Se valida la petición en la BD a través del Controlador y Repositorio de Login; si la contraseña falla, se deniega el acceso, y si acierta, se genera y retorna un Token JWT. [cite_start]Paralelamente, se ilustra el flujo alternativo de registro de un perfil completamente nuevo en la base de datos para habilitar el posterior inicio de sesión. [cite: 208]

## [cite_start]7.4 Diagrama del Mapa de Navegación [cite: 40]
> [cite_start]**Descripción del Mapa de Navegación:** Sirve para apreciar qué apartados del sistema están conectados entre sí y la cardinalidad de cada uno de ellos en la interfaz gráfica. [cite: 210] Se arranca desde el "Inicia sesión" hacia la "Pantalla principal". [cite_start]Desde ahí se desprenden rutas hacia "Servicios" (que conecta a "Publicar trabajo" o "Ver más"), hacia el "Buzón de chats" y el respectivo "Chat", o hacia el "Menú lateral", el cual otorga acceso a secciones de administración como "Mis trabajos aceptados" y "Mis publicaciones", detallando también los bucles de retroceso ("Regresar") para la navegación de usuario. [cite: 209]

---

# [cite_start]8. Punto de Vista de Recursos y Despliegue (Resource Viewpoint) [cite: 41]

## [cite_start]8.1 Propósito [cite: 42]
[cite_start]El propósito de este punto de vista es modelar la topología física sobre la cual operará el sistema MIZCUIN. [cite: 213] [cite_start]Ilustra cómo los artefactos de software (código compilado, scripts de Front-End y bases de datos) se mapean y distribuyen en el hardware y la infraestructura de red. [cite: 214] [cite_start]Además, documenta la estrategia de utilización de recursos para asegurar que la arquitectura cumpla con las restricciones de costo y rendimiento establecidas para la primera iteración. [cite: 215]

## [cite_start]8.2 Estrategia de Despliegue y Gestión de Recursos [cite: 43]
[cite_start]Para asegurar una portabilidad total y un entorno idéntico entre desarrollo y producción, la aplicación utiliza una estrategia de despliegue contenerizada. [cite: 217]
* [cite_start]**Infraestructura en la Nube:** El sistema principal se aloja en una única máquina virtual proporcionada por la capa gratuita de AWS EC2 (sistema operativo Linux). [cite: 218] [cite_start]Esta decisión centraliza los recursos y mantiene el costo operativo en cero durante la etapa inicial. [cite: 219]
* [cite_start]**Contenerización:** Se utiliza Docker (versión 29.2.1 o superior) para encapsular la aplicación. [cite: 220] [cite_start]Esto asegura que el código en Python y sus dependencias se ejecuten de manera aislada y eficiente. [cite: 221]
* [cite_start]**Proxy Inverso y Enrutamiento:** Las peticiones externas (tráfico de internet) no llegan directamente al servidor en Python. [cite: 222] [cite_start]Pasan primero por un servidor web Nginx, el cual actúa como proxy inverso, mejorando la seguridad, gestionando los certificados HTTPS y distribuyendo la carga de manera eficiente para garantizar el cumplimiento del RNF 2 (manejo de 50 consultas simultáneas sin superar el 95% de CPU). [cite: 223]

## [cite_start]8.3 Diagrama de Despliegue [cite: 44]
> [cite_start]**Descripción del Diagrama de Despliegue:** El diagrama de modelo físico visualiza en qué instancias se está ejecutando el código y cómo se distribuyen los componentes. [cite: 225] Por un lado se encuentra el "Dispositivo Móvil" del usuario con su navegador ejecutando la Aplicación Web (Front-End). Por el otro, conectado mediante internet, se expone un entorno en "Amazon Web Services (AWS)", específicamente en una "Instancia EC2". [cite_start]Adentro de la máquina virtual existe un "Contenedor: Proxy Web" con Nginx, que canaliza el tráfico al "Docker Engine", que contiene internamente el ejecutable de "Servidor API" en Python interactuando con su archivo nativo de base de datos "mizcuin.db" (SQLite 3.40.1+). [cite: 224]

## [cite_start]8.4 Descripción de los Nodos y Conexiones [cite: 45]
[cite_start]La arquitectura física se compone de dos grandes polos de procesamiento comunicados a través de Internet: [cite: 227]
* [cite_start]**Dispositivo Móvil (Nodo de Cliente) :** Representa el hardware del usuario final (Animal Lover). [cite: 228] [cite_start]Para garantizar la usabilidad (RNF 7), el dispositivo debe contar con un navegador moderno basado en Chromium. [cite: 229] [cite_start]Este nodo es el responsable de descargar y ejecutar los archivos estáticos del Front-End (JavaScript, HTML, CSS) y consumir los recursos de memoria locales del teléfono para mantener la caché activa. [cite: 230]
* [cite_start]**Instancia AWS EC2 (Nodo de Servidor) :** La máquina virtual en la nube que sostiene todo el procesamiento. [cite: 231]
    * [cite_start]Docker Engine: Administra los contenedores virtuales y los aísla del sistema operativo anfitrión para evitar conflictos de librerías y facilitar futuras migraciones. [cite: 232]
    * Contenedor Nginx: Expuesto a Internet. [cite_start]Intercepta el tráfico seguro (HTTPS) y actúa como un escudo protector, transfiriendo únicamente el tráfico API válido hacia el contenedor de la aplicación. [cite: 233]
    * [cite_start]Contenedor de Aplicación (Python + SQLite): Contiene el ejecutable compilado del servidor en Python. [cite: 234] [cite_start]Debido a la naturaleza de SQLite, la base de datos no requiere un contenedor o nodo separado; [cite: 235] [cite_start]se aloja simplemente como el archivo dentro del mismo contenedor lógico, permitiendo velocidades de lectura/escritura (I/O) altas. [cite: 236]

---

# [cite_start]9. Razón de Diseño y Trade-offs (Design Rationale) [cite: 46]

## [cite_start]9.1 Propósito [cite: 47]
[cite_start]El propósito de esta sección es documentar el razonamiento técnico que condujo a la arquitectura del sistema tal como fue diseñada. [cite: 239] [cite_start]Un Trade-off (compromiso de diseño) representa una decisión consciente en la que el equipo de desarrollo acepta una desventaja o limitación técnica en un área específica, a cambio de obtener un beneficio estratégico mayor que garantice el cumplimiento de los objetivos del negocio y los requerimientos no funcionales (costo, tiempo y recursos). [cite: 240]

## [cite_start]9.2 Tabla de decisiones [cite: 48]

| Decisión Arquitectónica | Alternativa Descartada | Ventaja Obtenida (El beneficio) | Desventaja Aceptada (El sacrificio / Riesgo) | Justificación para el Proyecto |
|---|---|---|---|---|
| Uso de tecnologías puras (Vanilla JS, HTML, CSS) en Front-End. | Frameworks o librerías complejas (ej. React, Angular, Vue). | Agilidad y ligereza: Se elimina la curva de aprendizaje, la configuración de empaquetadores (Webpack/Vite) y se agiliza drásticamente el desarrollo del producto para cumplir con el hito de un mes. | Código Front-End menos estructurado para escalar a largo plazo; mayor esfuerzo manual para manipular el DOM. | La prioridad absoluta es la velocidad de entrega y la validación funcional. [cite_start]La lógica visual requerida actualmente no justifica el peso ni la complejidad de un framework robusto. [cite: 242] |
| Almacenamiento de imágenes como BLOB en la Base de Datos. | Uso de servicios de almacenamiento en la nube externos (ej. Amazon S3, Cloudinary). | Simplicidad de despliegue : Se evita por completo la configuración, autenticación y gestión de servicios externos, manteniendo todo el ecosistema (datos y archivos) en un solo lugar. | Crecimiento acelerado del tamaño del archivo físico de la base de datos, lo que a futuro podría impactar los tiempos de respaldo. | [cite_start]En esta etapa temprana, se sacrifica la eficiencia de almacenamiento a largo plazo a cambio de garantizar un entorno de implementación rápido, económico y sin dependencias de red externas. [cite: 242] |
| Uso de SQLite como motor de Base de Datos. | Sistemas de Gestión de Bases de Datos Robustos (ej. PostgreSQL, MySQL). | Cero costos y bajo consumo: Al ser un motor embebido, no requiere un servidor independiente, consumiendo recursos mínimos de RAM y CPU en la capa gratuita de AWS EC2. | Concurrencia limitada; SQLite no está diseñado para manejar miles de escrituras simultáneas por segundo. | [cite_start]El volumen de tráfico proyectado para la red de Animal Lovers en sus primeras fases es bajo/moderado, por lo que SQLite es más que suficiente para cumplir con el RNF 2 sin generar costos de facturación en AWS. [cite: 242] |
| Arquitectura Monolítica Modular (Python). | Arquitectura de Microservicios distribuidos. | Facilidad de gestión : Un solo ejecutable y un solo contenedor Docker para monitorear, probar y desplegar, simplificando la gestión del repositorio en GitHub. | Si un módulo interno (ej. Chat) sufre una falla fatal que detiene el proceso, todo el servidor API (incluyendo Publicaciones) se caerá. | El equipo consta de 4 desarrolladores. [cite_start]La sobrecarga operativa (DevOps) de gestionar múltiples microservicios pondría en riesgo las fechas de entrega del Plan de Proyecto. [cite: 242] |