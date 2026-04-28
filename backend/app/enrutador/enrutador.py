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
from modelos.modelos import AnimalLoverLogin, AnimalLover, Trabajo, TrabajoAceptado, Mensaje, Albergue, AnimalPerdido, AnimalCalle
from manejadores import gestionUsuario, gestionTrabajo, gestionTrabajosAceptados, gestionMensajes, gestionAlbergues, gestionMasPerdidas, gestionAdopciones, gestionImagenes
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

@app.get("/albergue", dependencies=[Depends(validarSesion)])
def obtenerAlbergue(id: int):
    detalle, encontrado = gestionAlbergues.obtenerAlbergue(id)
    if not encontrado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="albergue no encontrado")
    return detalle

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

@app.get("/animal/{id_animal}/imagen")
def obtenerImagenAnimal(id_animal: int):
    imagen, encontrado = gestionImagenes.obtenerImagenAnimal(id_animal)
    if not encontrado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Imagen no encontrada")
    return Response(content=imagen, media_type="image/jpeg")

@app.get("/animal/{id_animal}/imagenes_info")
def obtenerInfoImagenesAnimal(id_animal: int):
    return gestionImagenes.obtenerInfoImagenesAnimal(id_animal)

@app.get("/animal/{id_animal}/imagen_index/{index}")
def obtenerImagenAnimalPorIndice(id_animal: int, index: int):
    imagen, encontrado = gestionImagenes.obtenerImagenAnimalPorIndice(id_animal, index)
    if not encontrado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Imagen no encontrada")
    return Response(content=imagen, media_type="image/jpeg")

@app.get("/albergue/{id_albergue}/imagen")
def obtenerImagenAlbergue(id_albergue: int):
    imagen, encontrado = gestionImagenes.obtenerImagenAlbergue(id_albergue)
    if not encontrado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Imagen no encontrada")
    return Response(content=imagen, media_type="image/jpeg")

@app.get("/albergue/{id_albergue}/imagenes_info")
def obtenerInfoImagenesAlbergue(id_albergue: int):
    return gestionImagenes.obtenerInfoImagenesAlbergue(id_albergue)

@app.get("/albergue/{id_albergue}/imagen_index/{index}")
def obtenerImagenAlberguePorIndice(id_albergue: int, index: int):
    imagen, encontrado = gestionImagenes.obtenerImagenAlberguePorIndice(id_albergue, index)
    if not encontrado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Imagen no encontrada")
    return Response(content=imagen, media_type="image/jpeg")

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

# ==================== COMUNIDAD: ALBERGUES ====================

@app.post("/albergues", status_code=status.HTTP_201_CREATED, dependencies=[Depends(validarSesion)])
def crear_albergue(albergue: Albergue):
    if not gestionAlbergues.crearAlbergue(albergue):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="no se pudo crear el albergue")
    return {"mensaje": "albergue creado correctamente"}

@app.get("/albergues", dependencies=[Depends(validarSesion)])
def obtener_albergues():
    lista, encontrado = gestionAlbergues.obtenerTodosLosAlbergues()
    if not encontrado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="no se encontraron albergues")
    return lista

@app.get("/albergues/detalle", dependencies=[Depends(validarSesion)])
def obtener_albergue_por_id(id_albergue: int):
    detalle, encontrado = gestionAlbergues.obtenerAlbergue(id_albergue)
    if not encontrado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="albergue no encontrado")
    return detalle

@app.put("/albergues", dependencies=[Depends(validarSesion)])
def actualizar_albergue(albergue: Albergue):
    if not gestionAlbergues.actualizarAlbergue(albergue):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="no se pudo actualizar el albergue")
    return {"mensaje": "albergue actualizado correctamente"}

@app.delete("/albergues", dependencies=[Depends(validarSesion)])
def eliminar_albergue(id_albergue: int):
    if not gestionAlbergues.eliminarAlbergue(id_albergue):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="no se pudo eliminar el albergue")
    return {"mensaje": "albergue eliminado correctamente"}

# ==================== COMUNIDAD: MASCOTAS PERDIDAS ====================

@app.post("/mascotas_perdidas", status_code=status.HTTP_201_CREATED, dependencies=[Depends(validarSesion)])
def crear_mascota_perdida(mascota: AnimalPerdido):
    if not gestionMasPerdidas.reportarMascotaPerdida(mascota):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="no se pudo reportar la mascota perdida")
    return {"mensaje": "mascota perdida reportada correctamente"}

@app.get("/mascotas_perdidas", dependencies=[Depends(validarSesion)])
def obtener_mascotas_perdidas():
    lista, encontrado = gestionMasPerdidas.obtenerMascotasPerdidas()
    if not encontrado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="no se encontraron mascotas perdidas")
    return lista

@app.get("/mascotas_perdidas/mis", dependencies=[Depends(validarSesion)])
def obtener_mascotas_perdidas_mias(idAnimalLover: int):
    lista, _ = gestionMasPerdidas.obtenerMascotasPerdidasPorUsuario(idAnimalLover)
    return lista

@app.get("/mascotas_perdidas/detalle", dependencies=[Depends(validarSesion)])
def obtener_mascota_perdida_detalle(id_animal: int):
    detalle, encontrado = gestionMasPerdidas.obtenerMascotaPerdida(id_animal)
    if not encontrado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="mascota perdida no encontrada")
    return detalle

@app.put("/mascotas_perdidas", dependencies=[Depends(validarSesion)])
def actualizar_mascota_perdida(mascota: AnimalPerdido):
    if not gestionMasPerdidas.actualizarMascotaPerdida(mascota):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="no se pudo actualizar la mascota perdida")
    return {"mensaje": "mascota perdida actualizada correctamente"}

@app.post("/mascotas_perdidas/localizado", dependencies=[Depends(validarSesion)])
def marcar_mascota_localizada(id_animal: int):
    if not gestionMasPerdidas.marcarMascotaLocalizada(id_animal):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="no se pudo marcar la mascota como localizada")
    return {"mensaje": "mascota marcada como localizada"}

@app.delete("/mascotas_perdidas", dependencies=[Depends(validarSesion)])
def eliminar_mascota_perdida(id_animal: int):
    if not gestionMasPerdidas.eliminarMascotaPerdida(id_animal):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="no se pudo eliminar la mascota perdida")
    return {"mensaje": "mascota perdida eliminada correctamente"}

# ==================== COMUNIDAD: ADOPCIONES ====================

@app.post("/adopciones", status_code=status.HTTP_201_CREATED, dependencies=[Depends(validarSesion)])
def crear_adopcion(adopcion: AnimalCalle):
    if not gestionAdopciones.publicarAdopcion(adopcion):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="no se pudo publicar la adopción")
    return {"mensaje": "adopción publicada correctamente"}

@app.get("/adopciones", dependencies=[Depends(validarSesion)])
def obtener_adopciones():
    lista, encontrado = gestionAdopciones.obtenerAdopciones()
    if not encontrado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="no se encontraron adopciones")
    return lista

@app.get("/adopciones/mis", dependencies=[Depends(validarSesion)])
def obtener_adopciones_mias(idAnimalLover: int):
    lista, _ = gestionAdopciones.obtenerAdopcionesPorUsuario(idAnimalLover)
    return lista

@app.get("/adopciones/detalle", dependencies=[Depends(validarSesion)])
def obtener_adopcion_detalle(id_animal: int):
    detalle, encontrado = gestionAdopciones.obtenerAdopcion(id_animal)
    if not encontrado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="adopcion no encontrada")
    return detalle

@app.put("/adopciones", dependencies=[Depends(validarSesion)])
def actualizar_adopcion(adopcion: AnimalCalle):
    if not gestionAdopciones.actualizarAdopcion(adopcion):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="no se pudo actualizar la adopcion")
    return {"mensaje": "adopcion actualizada correctamente"}

@app.post("/adopciones/adoptado", dependencies=[Depends(validarSesion)])
def marcar_adopcion_adoptada(id_animal: int):
    if not gestionAdopciones.marcarAdopcionAdoptada(id_animal):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="no se pudo marcar la adopcion como adoptada")
    return {"mensaje": "adopcion marcada como adoptada"}

@app.delete("/adopciones", dependencies=[Depends(validarSesion)])
def eliminar_adopcion(id_animal: int):
    if not gestionAdopciones.eliminarAdopcion(id_animal):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="no se pudo eliminar la adopcion")
    return {"mensaje": "adopcion eliminada correctamente"}

def IniciarServidor():
    print("Servidor iniciado en el puerto 40000")
    uvicorn.run(app, host="0.0.0.0", port=40000)

if __name__ == "__main__":
    IniciarServidor()
