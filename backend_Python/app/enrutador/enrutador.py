from fastapi import FastAPI, HTTPException, Depends, Header, status
from pydantic import BaseModel
from typing import Any, Dict, List, Optional
import uvicorn

# Importamos la logica de manejo de sesiones (autenticacion) desde nuestro otro archivo Python
from AuthMiddleware import crear_sesion, validar_sesion

# Inicializamos la instancia principal de la aplicacion FastAPI
# Esta variable 'app' es la que manejara todas las conexiones y rutas web como enrutador
app = FastAPI(title="API TSP_HellDevs")


# ==================== MODELOS BASE (Pydantic adaptado a sentencia.sql) ====================
# Pydantic se encarga de convertir (parsear) y validar automaticamente el texto en JSON 
# que llega dentro del BODY de las peticiones HTTP (hace lo mismo que la funcion 'utils.Convertir' en Go).

# Modelo usado exclusivamente para recibir las credenciales al intentar hacer Login
class UsuarioLogin(BaseModel):
    email: str
    contraseña: str

# Modelo que representa por completo a un Usuario, identico a la tabla en la base de datos
class Usuario(BaseModel):
    id_usuario: Optional[int] = None # Es Opcional porque al momento de crearlo (Registro), aun no tiene un ID
    nombre: str
    apellido: str
    email: str
    telefono: str
    contraseña: str
    token: Optional[str] = None

# Modelo para representar detalladamente la estructura de la tabla de Trabajo
class Trabajo(BaseModel):
    id_trabajo: Optional[int] = None
    nombre: str
    ubicacion: str
    fecha_publicacion: str
    monto: float
    descripcion: str
    id_usuario: int
    tipo_trabajo: str
    estado: str

# Modelo intermedio que sirve para procesar cuando un trabajo es tomado o concluido por alguien mas
class TrabajoAceptado(BaseModel):
    id_trabajo: int
    id_usuario: int
    fecha_aceptacion: str
    estado_trabajo: str  # Segun SQL: CHECK(estado_trabajo IN ("Pendiente", "Terminado", "Cancelado"))

# Modelo respectivo para el servicio de interaccion o chat de mensajería
class Mensaje(BaseModel):
    id_mensaje: Optional[int] = None
    id_usuario_envia: int
    id_usuario_recibe: int
    id_trabajo: int
    contenido: str
    fecha_mensaje: str


# ==================== RUTAS DE AUTENTICACION Y LOGIN (Publica) ====================

# El decorador @app.post("/login") indica que este bloque responde al metodo POST en la direccion o url '/login'
@app.post("/login")
def login_handler(usuario_login: UsuarioLogin):
    """ Este metodo recibe correo y contraseña; si son validos devuelve un Token de acceso """
    
    # AQUI IRIA LA CLASE DE MANEJOS DE BD (ej. RepositorioUsuario o ManejadorUsuario)
    
    # CODIGO BASE SIMULADO (MOCK) PARA MODIFICAR DESPUES
    encontrado = True # Simula que encontramos el usuario en la consulta a Base de Datos
    usuario_db = Usuario(
        id_usuario=1, nombre="Test", apellido="User", 
        email=usuario_login.email, telefono="123456", 
        contraseña="password"  # Asume que esta es la contraseña devuelta por SQLite o base de datos
    )
    
    # Verificamos si la validacion fallo (No lo encontro, o la clave es incorrecta)
    if not encontrado or usuario_db.contraseña != usuario_login.contraseña:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="email o contraseña incorrectos"
        )
    
    # Si todo es correcto, generamos un token utilizando nuestra funcion del modulo AuthMiddleware
    token = crear_sesion(usuario_db.id_usuario)
    
    # Retornamos los datos principales. En FastAPI, los JSON se construyen retornando un simple diccionario
    return {
        "token": token,
        "id_usuario": usuario_db.id_usuario,
        "nombre": f"{usuario_db.nombre} {usuario_db.apellido}"
    }


# ==================== RUTAS DE USUARIOS ====================

@app.post("/usuario", status_code=status.HTTP_201_CREATED)
def registrar_usuario(usuario: Usuario):
    """ Endpoint publico llamado cuando quieres registrar un nuevo usuario en la app (Signup) """
    
    # AQUI IRIA LA CLASE DE MANEJOS DE BD para guardar (ManejadorUsuario)
    
    # CODIGO BASE PARA MODIFICAR DESPUES
    ok = True
    if not ok:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="no se pudo registrar el usuario")
    return {"mensaje": "usuario registrado correctamente"}


@app.get("/usuario")
def obtener_usuario(id: int):
    """ Busca un usuario especifico basandose en el Query Parameter de la url (Ej. /usuario?id=1) """
    # En FastAPI colocar 'id: int' arriba atrapa automaticamente de la URL lo que venga en 'id'
    
    # AQUI IRIA LA CLASE DE MANEJOS DE BD para buscar un usuario por su identificar unico id
    
    # CODIGO BASE PARA MODIFICAR DESPUES
    encontrado = True
    if not encontrado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="usuario no encontrado")
    
    usuario_db = Usuario(
        id_usuario=id, nombre="Test", apellido="User", 
        email="test@test.com", telefono="123456", 
        contraseña="" # Vaciamos explicitamente la contraseña para jamas enviarla en la respuesta
    )
    return usuario_db


@app.put("/usuario")
def actualizar_usuario(usuario: Usuario):
    """ Modifica la informacion de un usuario proporcionando sus nuevos datos como JSON """
    
    # AQUI IRIA LA CLASE DE MANEJOS DE BD para aplicarle un update al usuario
    
    # CODIGO BASE PARA MODIFICAR DESPUES
    ok = True
    if not ok:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="no se pudo actualizar el usuario")
    return {"mensaje": "usuario actualizado correctamente"}


@app.delete("/usuario")
def eliminar_usuario(usuario: Usuario):
    """ Solicita dar de baja permanentemente una cuenta de usuario """
    
    # AQUI IRIA LA CLASE DE MANEJOS DE BD para ejecutar la eliminacion 
    
    # CODIGO BASE PARA MODIFICAR DESPUES
    ok = True
    if not ok:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="no se pudo eliminar el usuario")
    return {"mensaje": "usuario eliminado correctamente"}


# ==================== TRABAJOS PROTEGIDOS (Rutas con Sesion Activa) ====================

# NOTA CLAVE AQUÍ: Agregar "dependencies=[Depends(validar_sesion)]" simula la barrera 'validarSesion' de tu version Go.
# Si la peticion no incluye el Token o es invalido, jamas pasara hacia la ejecución de la función y responderá error 401.

@app.post("/trabajo", status_code=status.HTTP_201_CREATED, dependencies=[Depends(validar_sesion)])
def crear_trabajo(trabajo: Trabajo):
    """ Inserta o crea la solicitud de un nuevo trabajo a realizar en la base de datos (requiere login) """
    
    # AQUI IRIA LA CLASE DE MANEJOS DE BD (ManejadorTrabajo) para insert 
    
    ok = True
    if not ok:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="no se pudo crear el trabajo")
    return {"mensaje": "trabajo creado correctamente"}


@app.get("/trabajo", dependencies=[Depends(validar_sesion)])
def obtener_trabajo(id: int):
    """ Recibe un ID y obtiene la información del trabajo publicado en base al ID """
    
    # AQUI IRIA LA CLASE DE MANEJOS DE BD (ManejadorTrabajo) para buscar o realizar select 
    
    encontrado = True
    if not encontrado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="trabajo no encontrado")
    
    return Trabajo(
        id_trabajo=id, nombre="Ejemplo Trabajo", ubicacion="Ubicacion",
        fecha_publicacion="2026-04-19", monto=100.5, descripcion="Ejemplo Desc",
        id_usuario=1, tipo_trabajo="Tipo", estado="Activo"
    )


@app.put("/trabajo", dependencies=[Depends(validar_sesion)])
def actualizar_trabajo(trabajo: Trabajo):
    """ Aplica un cambio o actualización en los detalles del trabajo (Ubicación, Descripción, Monto) """
    
    # AQUI IRIA LA CLASE DE MANEJOS DE BD (ManejadorTrabajo) para la operacion update
    
    ok = True
    if not ok:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="no se pudo actualizar el trabajo")
    return {"mensaje": "trabajo actualizado correctamente"}


@app.delete("/trabajo", dependencies=[Depends(validar_sesion)])
def eliminar_trabajo(trabajo: Trabajo):
    """ Remueve completamente la publicacion del trabajo del sistema """
    
    # AQUI IRIA LA CLASE DE MANEJOS DE BD (ManejadorTrabajo) para ejecutar drop/delete
    
    ok = True
    if not ok:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="no se pudo eliminar el trabajo")
    return {"mensaje": "trabajo eliminado correctamente"}


# ==================== GESTION DE TRABAJOS ACEPTADOS ====================

@app.post("/trabajo-aceptado", status_code=status.HTTP_201_CREATED, dependencies=[Depends(validar_sesion)])
def aceptar_trabajo(trabajo: TrabajoAceptado):
    """ Efectua la accion de marcar un trabajo general como aceptado uniendo al id del trabajador """
    
    # AQUI IRIA LA CLASE DE MANEJOS DE BD (ManejadorTrabajoAceptado) para insertar la decision
    
    ok = True
    if not ok:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="no se pudo aceptar el trabajo")
    return {"mensaje": "trabajo aceptado correctamente"}


@app.get("/trabajo-aceptado", dependencies=[Depends(validar_sesion)])
def listar_trabajos_aceptados(id_usuario: int):
    """ Retorna todos los trabajos que un usuario actualmente decidio aceptar y realizar """
    
    # AQUI IRIA LA CLASE DE MANEJOS DE BD (ManejadorTrabajoAceptado) para recuperar la lista de uno especifico
    
    encontrado = True
    if not encontrado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="no se encontraron trabajos aceptados")
    return [] # Aquí vas a retornar la lista llena proveniente de la Base de Datos


@app.put("/trabajo-aceptado", dependencies=[Depends(validar_sesion)])
def actualizar_trabajo_aceptado(trabajo: TrabajoAceptado):
    """ Cambia o altera los estados (Si paso de "Pendiente" a "Terminado") de un encargo aceptado """
    
    # AQUI IRIA LA CLASE DE MANEJOS DE BD (ManejadorTrabajoAceptado) para modificar estado
    
    ok = True
    if not ok:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="no se pudo actualizar el trabajo aceptado")
    return {"mensaje": "trabajo aceptado actualizado correctamente"}


@app.delete("/trabajo-aceptado", dependencies=[Depends(validar_sesion)])
def eliminar_trabajo_aceptado(trabajo: TrabajoAceptado):
    """ Revierte la operacion. El usuario cancela su intencion o borra que acepto un trabajo """
    
    # AQUI IRIA LA CLASE DE MANEJOS DE BD (ManejadorTrabajoAceptado) para deshacer
    
    ok = True
    if not ok:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="no se pudo eliminar el trabajo aceptado")
    return {"mensaje": "trabajo aceptado eliminado correctamente"}


# ==================== SECCION DE MENSAGERIA / CHAT_ID ====================

@app.post("/mensaje", status_code=status.HTTP_201_CREATED, dependencies=[Depends(validar_sesion)])
def enviar_mensaje(mensaje: Mensaje):
    """ Inserta o "envia" un nuevo mensaje entre el empleado y empleador en un trabajo actual """
    
    # AQUI IRIA LA CLASE DE MANEJOS DE BD (ManejadorMensaje) guardando las cadenas de texto (id_envia->id_recibe)
    
    ok = True
    if not ok:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="no se pudo enviar el mensaje")
    return {"mensaje": "mensaje enviado correctamente"}


@app.get("/mensaje", dependencies=[Depends(validar_sesion)])
def listar_mensajes(id_usuario: int, id_trabajo: int):
    """ Devuelve el hilo completo de la conversacion filtrado por un ID de Trabajo y el Usuario actual """
    # Nota: Los parametros vienen directamente de la url asi /mensaje?id_usuario=X&id_trabajo=X 
    
    # AQUI IRIA LA CLASE DE MANEJOS DE BD (ManejadorMensaje) 
    
    encontrado = True
    if not encontrado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="no se encontraron mensajes")
    return [] # Mismo caso, un list() completo se retorna


@app.put("/mensaje", dependencies=[Depends(validar_sesion)])
def actualizar_mensaje(id_mensaje: int, mensaje: Mensaje):
    """ Metodo enfocado en editar y reflejar de inmediato los cambios de algun texto de un Mensaje """
    
    # AQUI IRIA LA CLASE DE MANEJOS DE BD (ManejadorMensaje) para actualizar su contenido textual
    
    ok = True
    if not ok:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="no se pudo actualizar el mensaje")
    return {"mensaje": "mensaje actualizado correctamente"}


@app.delete("/mensaje", dependencies=[Depends(validar_sesion)])
def eliminar_mensaje(id_mensaje: int):
    """ Elimina el mensaje por completo del registro y la historia basados en un identificador especifico """
    
    # AQUI IRIA LA CLASE DE MANEJOS DE BD (ManejadorMensaje) para borrar via id
    
    ok = True
    if not ok:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="no se pudo eliminar el mensaje")
    return {"mensaje": "mensaje eliminado correctamente"}


# ==================== MAIN PRINCIPAL ====================

def IniciarServidor():
    """ Arranca internamente el servidor HTTP en el puerto 40000 similar al http.ListenAndServe de Go """
    print("Servidor iniciado en el puerto 40000")
    
    # Levanta el servidor local o la interfaz publica 0.0.0.0 para escuchar todas las conexiones
    uvicorn.run(app, host="0.0.0.0", port=40000)

if __name__ == "__main__":
    IniciarServidor()
