from fastapi import FastAPI, HTTPException, Depends, Header, status
from pydantic import BaseModel
from typing import Any, Dict, List, Optional
import uvicorn

# Importamos la logica de middleware de autenticacion
from AuthMiddleware import crear_sesion, validar_sesion

# Inicializamos la aplicacion FastAPI
app = FastAPI(title="API TSP_HellDevs")

# ==================== MODELOS (Pydantic basados en sentencia.sql) ====================

class UsuarioLogin(BaseModel):
    email: str
    contraseña: str

class Usuario(BaseModel):
    id_usuario: Optional[int] = None
    nombre: str
    apellido: str
    email: str
    telefono: str
    contraseña: str
    token: Optional[str] = None

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

class TrabajoAceptado(BaseModel):
    id_trabajo: int
    id_usuario: int
    fecha_aceptacion: str
    estado_trabajo: str  # CHECK(estado_trabajo IN ("Pendiente", "Terminado", "Cancelado"))

class Mensaje(BaseModel):
    id_mensaje: Optional[int] = None
    id_usuario_envia: int
    id_usuario_recibe: int
    id_trabajo: int
    contenido: str
    fecha_mensaje: str

# ==================== LOGIN ====================

@app.post("/login")
def login_handler(usuario_login: UsuarioLogin):
    # AQUI IRIA LA CLASE DE MANEJOS DE BD (ej. ManejadorUsuario o RepositorioUsuario)
    # Por ejemplo:
    # repo_usuario = RepositorioUsuario()
    # usuario_db = repo_usuario.buscar_por_email(usuario_login.email)
    
    # CODIGO BASE PARA MODIFICAR DESPUES
    encontrado = True # Simular buscar
    usuario_db = Usuario(
        id_usuario=1, nombre="Test", apellido="User", 
        email=usuario_login.email, telefono="123456", 
        contraseña="password"  # Asume que esta es la obtenida de la BD
    )
    
    if not encontrado or usuario_db.contraseña != usuario_login.contraseña:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="email o contraseña incorrectos"
        )
    
    # genero un token y lo asocio al usuario
    token = crear_sesion(usuario_db.id_usuario)
    
    return {
        "token": token,
        "id_usuario": usuario_db.id_usuario,
        "nombre": f"{usuario_db.nombre} {usuario_db.apellido}"
    }

# ==================== USUARIOS ====================

@app.post("/usuario", status_code=status.HTTP_201_CREATED)
def registrar_usuario(usuario: Usuario):
    # AQUI IRIA LA CLASE DE MANEJOS DE BD para guardar (ManejadorUsuario)
    
    # CODIGO BASE PARA MODIFICAR DESPUES
    ok = True
    if not ok:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="no se pudo registrar el usuario")
    return {"mensaje": "usuario registrado correctamente"}

@app.get("/usuario")
def obtener_usuario(id: int):
    # AQUI IRIA LA CLASE DE MANEJOS DE BD para buscar usuario por id
    
    # CODIGO BASE PARA MODIFICAR DESPUES
    encontrado = True
    if not encontrado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="usuario no encontrado")
    
    usuario_db = Usuario(
        id_usuario=id, nombre="Test", apellido="User", 
        email="test@test.com", telefono="123456", 
        contraseña="" # no devuelvo la contraseña en la respuesta
    )
    return usuario_db

@app.put("/usuario")
def actualizar_usuario(usuario: Usuario):
    # AQUI IRIA LA CLASE DE MANEJOS DE BD para actualizar usuario
    
    # CODIGO BASE PARA MODIFICAR DESPUES
    ok = True
    if not ok:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="no se pudo actualizar el usuario")
    return {"mensaje": "usuario actualizado correctamente"}

@app.delete("/usuario")
def eliminar_usuario(usuario: Usuario):
    # AQUI IRIA LA CLASE DE MANEJOS DE BD para eliminar usuario
    
    # CODIGO BASE PARA MODIFICAR DESPUES
    ok = True
    if not ok:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="no se pudo eliminar el usuario")
    return {"mensaje": "usuario eliminado correctamente"}

# ==================== TRABAJOS (PUBLICACIONES) ====================

@app.post("/trabajo", status_code=status.HTTP_201_CREATED, dependencies=[Depends(validar_sesion)])
def crear_trabajo(trabajo: Trabajo):
    # AQUI IRIA LA CLASE DE MANEJOS DE BD (ManejadorTrabajo) para crear
    
    # CODIGO BASE PARA MODIFICAR DESPUES
    ok = True
    if not ok:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="no se pudo crear el trabajo")
    return {"mensaje": "trabajo creado correctamente"}

@app.get("/trabajo", dependencies=[Depends(validar_sesion)])
def obtener_trabajo(id: int):
    # AQUI IRIA LA CLASE DE MANEJOS DE BD (ManejadorTrabajo) para buscar
    
    # CODIGO BASE PARA MODIFICAR DESPUES
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
    # AQUI IRIA LA CLASE DE MANEJOS DE BD (ManejadorTrabajo) para actualizar
    
    # CODIGO BASE PARA MODIFICAR DESPUES
    ok = True
    if not ok:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="no se pudo actualizar el trabajo")
    return {"mensaje": "trabajo actualizado correctamente"}

@app.delete("/trabajo", dependencies=[Depends(validar_sesion)])
def eliminar_trabajo(trabajo: Trabajo):
    # AQUI IRIA LA CLASE DE MANEJOS DE BD (ManejadorTrabajo) para eliminar
    
    # CODIGO BASE PARA MODIFICAR DESPUES
    ok = True
    if not ok:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="no se pudo eliminar el trabajo")
    return {"mensaje": "trabajo eliminado correctamente"}

# ==================== TRABAJOS ACEPTADOS ====================

@app.post("/trabajo-aceptado", status_code=status.HTTP_201_CREATED, dependencies=[Depends(validar_sesion)])
def aceptar_trabajo(trabajo: TrabajoAceptado):
    # AQUI IRIA LA CLASE DE MANEJOS DE BD (ManejadorTrabajoAceptado) para insertar
    
    # CODIGO BASE PARA MODIFICAR DESPUES
    ok = True
    if not ok:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="no se pudo aceptar el trabajo")
    return {"mensaje": "trabajo aceptado correctamente"}

@app.get("/trabajo-aceptado", dependencies=[Depends(validar_sesion)])
def listar_trabajos_aceptados(id_usuario: int):
    # AQUI IRIA LA CLASE DE MANEJOS DE BD (ManejadorTrabajoAceptado) para obtener lista
    
    # CODIGO BASE PARA MODIFICAR DESPUES
    encontrado = True
    if not encontrado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="no se encontraron trabajos aceptados")
    return [] # retornar la lista real en su lugar

@app.put("/trabajo-aceptado", dependencies=[Depends(validar_sesion)])
def actualizar_trabajo_aceptado(trabajo: TrabajoAceptado):
    # AQUI IRIA LA CLASE DE MANEJOS DE BD (ManejadorTrabajoAceptado) para actualizar
    
    # CODIGO BASE PARA MODIFICAR DESPUES
    ok = True
    if not ok:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="no se pudo actualizar el trabajo aceptado")
    return {"mensaje": "trabajo aceptado actualizado correctamente"}

@app.delete("/trabajo-aceptado", dependencies=[Depends(validar_sesion)])
def eliminar_trabajo_aceptado(trabajo: TrabajoAceptado):
    # AQUI IRIA LA CLASE DE MANEJOS DE BD (ManejadorTrabajoAceptado) para eliminar
    
    # CODIGO BASE PARA MODIFICAR DESPUES
    ok = True
    if not ok:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="no se pudo eliminar el trabajo aceptado")
    return {"mensaje": "trabajo aceptado eliminado correctamente"}

# ==================== MENSAJES ====================

@app.post("/mensaje", status_code=status.HTTP_201_CREATED, dependencies=[Depends(validar_sesion)])
def enviar_mensaje(mensaje: Mensaje):
    # AQUI IRIA LA CLASE DE MANEJOS DE BD (ManejadorMensaje) para guardar
    
    # CODIGO BASE PARA MODIFICAR DESPUES
    ok = True
    if not ok:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="no se pudo enviar el mensaje")
    return {"mensaje": "mensaje enviado correctamente"}

@app.get("/mensaje", dependencies=[Depends(validar_sesion)])
def listar_mensajes(id_usuario: int, id_trabajo: int):
    # AQUI IRIA LA CLASE DE MANEJOS DE BD (ManejadorMensaje) para listar
    
    # CODIGO BASE PARA MODIFICAR DESPUES
    encontrado = True
    if not encontrado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="no se encontraron mensajes")
    return [] # retornar la lista real

@app.put("/mensaje", dependencies=[Depends(validar_sesion)])
def actualizar_mensaje(id_mensaje: int, mensaje: Mensaje):
    # AQUI IRIA LA CLASE DE MANEJOS DE BD (ManejadorMensaje) para actualizar
    
    # CODIGO BASE PARA MODIFICAR DESPUES
    ok = True
    if not ok:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="no se pudo actualizar el mensaje")
    return {"mensaje": "mensaje actualizado correctamente"}

@app.delete("/mensaje", dependencies=[Depends(validar_sesion)])
def eliminar_mensaje(id_mensaje: int):
    # AQUI IRIA LA CLASE DE MANEJOS DE BD (ManejadorMensaje) para eliminar
    
    # CODIGO BASE PARA MODIFICAR DESPUES
    ok = True
    if not ok:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="no se pudo eliminar el mensaje")
    return {"mensaje": "mensaje eliminado correctamente"}

def IniciarServidor():
    print("Servidor iniciado en el puerto 40000")
    uvicorn.run(app, host="0.0.0.0", port=40000)

if __name__ == "__main__":
    IniciarServidor()
