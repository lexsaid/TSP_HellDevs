# Resumen del Proyecto: TSP_HellDevs

Este documento proporciona el contexto general del proyecto y su arquitectura para que sirva como base en el diseño y ejecución de las pruebas de comportamiento (Behavior-Driven Development - BDD).

## 1. Descripción General del Negocio
**TSP_HellDevs** es una plataforma multifacética que conecta a usuarios mediante distintos módulos principales:
- **Gestión de Trabajos:** Permite a los usuarios ofrecer y buscar trabajos, y gestionar trabajos aceptados.
- **Gestión de Animales:** Incluye funcionalidades para adopciones de mascotas, gestión de albergues y reporte de mascotas perdidas.
- **Interacción y Mensajería:** Los usuarios pueden comunicarse mediante un sistema de mensajes internos.
- **Gestión de Medios:** Soporte para carga y visualización de imágenes (asociadas a mascotas, trabajos o usuarios).

## 2. Arquitectura del Sistema
El ecosistema del proyecto consta de múltiples implementaciones:

### Backend
Actualmente, el sistema cuenta con integraciones en dos tecnologías:
1. **Python (FastAPI):** Existe un backend en Python con una suite de pruebas activas (pytest) que valida endpoints de enrutamiento (`test_enrutador_routes.py`), seguridad (middleware de tokens en `test_auth_middleware.py`), y la lógica de negocio para adopciones, trabajos, y mascotas.
2. **Golang (Go):** Existe una versión del backend estructurada en capas (Controladores, Manejadores, Repositorios) que utiliza **SQLite** como base de datos. Funciona recibiendo peticiones JSON crudas e hidratando los modelos en memoria mediante utilidades personalizadas (`ManejadorJSON.go`).

### Frontend
El frontend está construido principalmente en HTML, CSS y JavaScript (con archivos como `pubAdopcion.html`), consumiendo las API provistas por el backend.

## 3. Seguridad y Autenticación
El sistema protege sus rutas privadas mediante un **Middleware de Autenticación**. 
- Los usuarios inician sesión y reciben un token (de 64 caracteres hexadecimales).
- Para acceder a recursos protegidos, el token debe ser incluido en las cabeceras HTTP. El middleware intercepta la petición, verifica el token y adjunta la identidad del usuario (`idUsuario` / `idAnimalLover`) al estado de la petición, o de lo contrario devuelve un error `401 Unauthorized`.

## 4. Próximos Pasos para Pruebas de Comportamiento (BDD)
Dado este contexto, en esta carpeta (`pruebas_de_comportamiento`) se deben colocar los archivos `.feature` (escritos en Gherkin) y los correspondientes *steps* en Python (usando `behave` o `pytest-bdd`) para validar los siguientes flujos End-to-End:
1. **Flujo de Usuario:** Registro, Inicio de Sesión y validación de tokens inválidos.
2. **Flujo de Trabajo:** Publicación de un trabajo, búsqueda y aceptación de ofertas.
3. **Flujo de Adopciones:** Registro de un albergue, publicación de mascota en adopción o mascota perdida.

> *Nota: Asegúrese de tener instaladas las dependencias correctas (`behave` o `pytest-bdd`) antes de ejecutar los escenarios y configurar los repositorios mockeados o la base de datos de pruebas (SQLite) para evitar alterar los datos de producción.*
