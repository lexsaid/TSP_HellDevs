from fastapi import FastAPI, HTTPException, Depends, Header, status, Response
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any
import uvicorn
import asyncio
from datetime import datetime, timedelta
try:
    from zoneinfo import ZoneInfo
except ImportError:
    from backports.zoneinfo import ZoneInfo # En caso de que se necesite soporte antiguo, aunque python 3.11 lo trae nativo.

from enrutador.AuthMiddleware import crearSesion, validarSesion
from modelos.modelos import AnimalLoverLogin, AnimalLover, Trabajo, TrabajoAceptado, Mensaje
from manejadores import gestionUsuario, gestionTrabajo, gestionTrabajosAceptados, gestionMensajes
from repositorios import usuarioRepo, imagenRepo

app = FastAPI(title="API TSP_HellDevs")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://www.mizcuin.online", 
        "https://mizcuin.online"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "Accept"],
)

async def resetTokensJob():
    tz = ZoneInfo("America/Mexico_City")
    while True:
        ahora = datetime.now(tz)
        proximoReset = ahora.replace(hour=1, minute=0, second=0, microsecond=0)
        
        if ahora >= proximoReset:
            # Si ya pasó la 1:00 AM de hoy, programar para mañana a la 1:00 AM
            proximoReset += timedelta(days=1)
            
        esperaSegundos = (proximoReset - ahora).total_seconds()
        print(f"Tokens reset programmed in {esperaSegundos} seconds (at {proximoReset} CDMX time)")
        
        await asyncio.sleep(esperaSegundos)
        
        # Ejecutar el reseteo
        usuarioRepo.resetearTodosLosTokens()
        print("Tokens reseteados exitosamente.")

@app.on_event("startup")
async def startupEvent():
    asyncio.create_task(resetTokensJob())

# ==================== RUTAS DE AUTENTICACION Y LOGIN ====================

@app.post("/login")
def loginHandler(animalLoverLogin: AnimalLoverLogin):
    usuarioDB, encontrado = usuarioRepo.buscarPorEmail(animalLoverLogin.email)
    
    if not encontrado or usuarioDB.contrasena != animalLoverLogin.contrasena:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="email o contraseña incorrectos"
        )
    
    token = crearSesion(usuarioDB.idAnimalLover)
    
    return {
        "token": token,
        "idAnimalLover": usuarioDB.idAnimalLover,
        "nombre": f"{usuarioDB.nombre} {usuarioDB.apellido}"
    }

# ==================== RUTAS DE USUARIOS ====================

@app.post("/animalLover", status_code=status.HTTP_201_CREATED)
def registrarAnimalLover(animalLover: AnimalLover):
    if not gestionUsuario.guardarUsuario(animalLover):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="no se pudo registrar el usuario")
    return {"mensaje": "usuario registrado correctamente"}

@app.get("/animalLover")
def obtenerAnimalLover(id: int):
    usuario, encontrado = gestionUsuario.buscarUsuario(id)
    if not encontrado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="usuario no encontrado")
    usuario.contrasena = "" # No enviar contraseña
    return usuario

@app.put("/animalLover")
def actualizarAnimalLover(animalLover: AnimalLover):
    if not gestionUsuario.actualizarUsuario(animalLover):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="no se pudo actualizar el usuario")
    return {"mensaje": "usuario actualizado correctamente"}

@app.delete("/animalLover")
def eliminarAnimalLover(id: int):
    if not gestionUsuario.eliminarUsuario(id):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="no se pudo eliminar el usuario")
    return {"mensaje": "usuario eliminado correctamente"}

# ==================== TRABAJOS PROTEGIDOS ====================

@app.post("/trabajo", status_code=status.HTTP_201_CREATED, dependencies=[Depends(validarSesion)])
def crearTrabajo(trabajo: Trabajo):
    if not gestionTrabajo.crearTrabajo(trabajo):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="no se pudo crear el trabajo")
    return {"mensaje": "trabajo creado correctamente"}

@app.get("/trabajo", dependencies=[Depends(validarSesion)])
def obtenerTrabajo(id: int):
    trabajo, encontrado = gestionTrabajo.obtenerTrabajo(id)
    if not encontrado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="trabajo no encontrado")
    return trabajo

@app.get("/trabajos", dependencies=[Depends(validarSesion)])
def obtenerTodosLosTrabajos():
    lista, encontrado = gestionTrabajo.obtenerTodosLosTrabajos()
    if not encontrado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="no se encontraron trabajos")
    return lista

@app.get("/trabajo/{id_trabajo}/imagen")
def obtenerImagenTrabajo(id_trabajo: int):
    consulta = "SELECT * FROM imagen WHERE id_trabajo = ?"
    imagenes, encontrado = imagenRepo.buscarImagenes(consulta, id_trabajo)
    if not encontrado or not imagenes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Imagen no encontrada")
    return Response(content=imagenes[0].imagen, media_type="image/jpeg")

@app.get("/trabajo/{id_trabajo}/imagenes_info")
def obtenerInfoImagenesTrabajo(id_trabajo: int):
    consulta = "SELECT * FROM imagen WHERE id_trabajo = ?"
    imagenes, encontrado = imagenRepo.buscarImagenes(consulta, id_trabajo)
    if not encontrado or not imagenes:
        return {"count": 0}
    return {"count": len(imagenes)}

@app.get("/trabajo/{id_trabajo}/imagen_index/{index}")
def obtenerImagenTrabajoPorIndice(id_trabajo: int, index: int):
    consulta = "SELECT * FROM imagen WHERE id_trabajo = ?"
    imagenes, encontrado = imagenRepo.buscarImagenes(consulta, id_trabajo)
    if not encontrado or not imagenes or index >= len(imagenes) or index < 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Imagen no encontrada")
    return Response(content=imagenes[index].imagen, media_type="image/jpeg")

@app.put("/trabajo", dependencies=[Depends(validarSesion)])
def actualizarTrabajo(trabajo: Trabajo):
    if not gestionTrabajo.actualizarTrabajo(trabajo):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="no se pudo actualizar el trabajo")
    return {"mensaje": "trabajo actualizado correctamente"}

@app.delete("/trabajo", dependencies=[Depends(validarSesion)])
def eliminarTrabajo(id: int):
    if not gestionTrabajo.eliminarTrabajo(id):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="no se pudo eliminar el trabajo")
    return {"mensaje": "trabajo eliminado correctamente"}

# ==================== GESTION DE TRABAJOS ACEPTADOS ====================

@app.post("/trabajo-aceptado", status_code=status.HTTP_201_CREATED, dependencies=[Depends(validarSesion)])
def aceptarTrabajo(trabajo: TrabajoAceptado):
    if not gestionTrabajosAceptados.aceptarTrabajo(trabajo):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="no se pudo aceptar el trabajo")
    return {"mensaje": "trabajo aceptado correctamente"}

@app.get("/trabajo-aceptado", dependencies=[Depends(validarSesion)])
def listarTrabajosAceptados(idAnimalLoverTrabajador: int):
    lista, encontrado = gestionTrabajosAceptados.obtenerListaTrabajosAceptados(idAnimalLoverTrabajador)
    if not encontrado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="no se encontraron trabajos aceptados")
    return lista

@app.put("/trabajo-aceptado", dependencies=[Depends(validarSesion)])
def actualizarTrabajoAceptado(trabajo: TrabajoAceptado):
    if not gestionTrabajosAceptados.actualizarTrabajoAceptado(trabajo):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="no se pudo actualizar el trabajo aceptado")
    return {"mensaje": "trabajo aceptado actualizado correctamente"}

@app.delete("/trabajo-aceptado", dependencies=[Depends(validarSesion)])
def eliminarTrabajoAceptado(idTrabajo: int, idAnimalLoverTrabajador: int):
    if not gestionTrabajosAceptados.eliminarTrabajoAceptado(idTrabajo, idAnimalLoverTrabajador):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="no se pudo eliminar el trabajo aceptado")
    return {"mensaje": "trabajo aceptado eliminado correctamente"}

@app.get("/trabajo-aceptado/check", dependencies=[Depends(validarSesion)])
def verificarTrabajoAceptado(idTrabajo: int):
    """Verifica si un trabajo ya fue aceptado y/o completado."""
    return gestionTrabajosAceptados.verificarTrabajoAceptado(idTrabajo)

@app.post("/trabajo-aceptado/completar", dependencies=[Depends(validarSesion)])
def completarTrabajo(idTrabajo: int):
    """El publicador marca su trabajo como completado — actualiza el registro del trabajador a Terminado."""
    if not gestionTrabajosAceptados.completarTrabajoPorPublicador(idTrabajo):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="no se pudo completar el trabajo")
    return {"mensaje": "trabajo marcado como completado"}


# ==================== SECCION DE MENSAJERIA ====================

@app.post("/mensaje", status_code=status.HTTP_201_CREATED, dependencies=[Depends(validarSesion)])
def enviarMensaje(mensaje: Mensaje):
    if not gestionMensajes.guardarMensaje(mensaje):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="no se pudo enviar el mensaje")
    return {"mensaje": "mensaje enviado correctamente"}

@app.get("/mensaje", dependencies=[Depends(validarSesion)])
def listarMensajes(idAnimalLover: int, idOtroAnimalLover: int, idTrabajo: int):
    lista, encontrado = gestionMensajes.obtenerListaMensajes(idAnimalLover, idOtroAnimalLover, idTrabajo)
    if not encontrado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="no se encontraron mensajes")
    return lista

@app.get("/chats", dependencies=[Depends(validarSesion)])
def listarChatsPrevios(idAnimalLover: int):
    lista, encontrado = gestionMensajes.obtenerChatsPrevios(idAnimalLover)
    # If no chats found, it just returns empty list, not necessarily 404
    return lista

@app.get("/mensajes/hay-nuevos", dependencies=[Depends(validarSesion)])
def hayNuevosMensajes(idAnimalLover: int, ultimoIdMensaje: int = 0):
    """Verifica si hay mensajes nuevos enviados a este usuario después del ID dado."""
    resultado = gestionMensajes.hayNuevosMensajes(idAnimalLover, ultimoIdMensaje)
    return {"hayNuevos": resultado}

@app.put("/mensaje", dependencies=[Depends(validarSesion)])
def actualizarMensaje(idMensaje: int, contenido: str):
    if not gestionMensajes.actualizarMensaje(idMensaje, contenido):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="no se pudo actualizar el mensaje")
    return {"mensaje": "mensaje actualizado correctamente"}

@app.delete("/mensaje", dependencies=[Depends(validarSesion)])
def eliminarMensaje(idMensaje: int):
    if not gestionMensajes.eliminarMensaje(idMensaje):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="no se pudo eliminar el mensaje")
    return {"mensaje": "mensaje eliminado correctamente"}

def IniciarServidor():
    print("Servidor iniciado en el puerto 40000")
    uvicorn.run(app, host="0.0.0.0", port=40000)

if __name__ == "__main__":
    IniciarServidor()
