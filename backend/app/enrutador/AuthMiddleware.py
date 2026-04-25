import os
import binascii
from fastapi import HTTPException, Header, status, Request
from repositorios import usuarioRepo

# ==================== MIDDLEWARE DE AUTENTICACION ====================

def generarToken() -> str:
    """
    Genera un token aleatorio seguro de 32 bytes y lo convierte a formato hexadecimal.
    """
    return binascii.hexlify(os.urandom(32)).decode('utf-8')

def crearSesion(idAnimalLover: int) -> str:
    """
    Crea una sesion nueva actualizando el token en la base de datos para el usuario especificado.
    Retorna el token para que pueda ser enviado al cliente.
    """
    token = generarToken()
    if usuarioRepo.actualizarToken(idAnimalLover, token):
        return token
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al guardar el token de sesión"
        )

def eliminarSesion(token: str):
    """
    Elimina la sesion activa actualizando el token a NULL en la base de datos.
    """
    usuario, encontrado = usuarioRepo.buscarPorToken(token)
    if encontrado and usuario:
        usuarioRepo.actualizarToken(usuario.idAnimalLover, None)

def validarSesion(request: Request, authorization: str = Header(None)) -> int:
    """
    Dependencia de FastAPI (Middleware). Se ejecuta ANTES de que la peticion llegue al controlador final.
    """
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="No se envió el token de autenticación"
        )
    
    usuario, encontrado = usuarioRepo.buscarPorToken(authorization)
    
    if not encontrado or not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Token inválido o sesión expirada"
        )
    
    request.state.idUsuario = usuario.idAnimalLover
    return usuario.idAnimalLover
