import os
import binascii
from fastapi import HTTPException, Header, status, Request
from typing import Dict

# aqui guardo las sesiones activas: token -> id_usuario
sesiones: Dict[str, int] = {}

def generar_token() -> str:
    """genero un token aleatorio de 32 bytes en hexadecimal para usarlo como identificador de sesion"""
    return binascii.hexlify(os.urandom(32)).decode('utf-8')

def crear_sesion(id_usuario: int) -> str:
    """creo una sesion nueva para el usuario y le devuelvo el token generado"""
    token = generar_token()
    sesiones[token] = id_usuario
    return token

def eliminar_sesion(token: str):
    """elimino la sesion del usuario cuando cierra sesion"""
    if token in sesiones:
        del sesiones[token]

def validar_sesion(request: Request, authorization: str = Header(None)) -> int:
    """
    verifico que el token sea valido antes de dejar pasar la solicitud
    si es valido, devuelvo el id_usuario para que los handlers lo puedan usar
    """
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="no se envio el token de autenticacion"
        )
    
    id_usuario = sesiones.get(authorization)
    
    if id_usuario is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="token invalido o sesion expirada"
        )
    
    # paso el id_usuario mediante el estado del request por si se ocupa
    request.state.id_usuario = id_usuario
    return id_usuario
