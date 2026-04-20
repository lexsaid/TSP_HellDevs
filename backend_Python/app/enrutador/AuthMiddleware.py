import os
import binascii
from fastapi import HTTPException, Header, status, Request
from typing import Dict

# ==================== MIDDLEWARE DE AUTENTICACION ====================
# Este archivo maneja la logica de sesiones simulando la verificacion por tokens.
# Funciona similar a como lo hacia AuthMiddleware.go.

# Diccionario en memoria donde se guardan las sesiones activas. 
# Actua como una base de datos temporal donde la llave es el 'token' y el valor es el 'id_usuario'.
sesiones: Dict[str, int] = {}

def generar_token() -> str:
    """
    Genera un token aleatorio seguro de 32 bytes y lo convierte a formato hexadecimal.
    Este token es utilizado como el identificador unico de sesion para un usuario.
    Al usar os.urandom es altamente seguro e impredecible.
    """
    return binascii.hexlify(os.urandom(32)).decode('utf-8')

def crear_sesion(id_usuario: int) -> str:
    """
    Crea una sesion nueva asociando el id de un usuario con un token recien generado.
    Retorna el token para que pueda ser enviado al cliente (por ejemplo, al iniciar sesion correctamente).
    """
    token = generar_token()
    sesiones[token] = id_usuario
    return token

def eliminar_sesion(token: str):
    """
    Elimina la sesion activa de la memoria buscando el token en el diccionario.
    Util para implementar la funcionalidad real de "Cerrar sesion (Log out)".
    """
    if token in sesiones:
        del sesiones[token]

def validar_sesion(request: Request, authorization: str = Header(None)) -> int:
    """
    Dependencia de FastAPI (Middleware). Se ejecuta ANTES de que la peticion llegue al controlador final.
    
    1. Verifica que el cliente haya enviado la cabecera 'Authorization' con un token al servidor.
    2. Busca el token en el diccionario interno de 'sesiones'.
    3. Si es invalido o expirado, interrumpe y rechaza la peticion devolviendo un error 401.
    4. Si es valido, devuelve el 'id_usuario' que tambien se inyecta en el estado interno del request.
    """
    # Validacion 1: Comprobar si el header de autorizacion viene vacio
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="no se envio el token de autenticacion"
        )
    
    # Validacion 2: Buscar a que usuario le pertenece este token
    id_usuario = sesiones.get(authorization)
    
    # Validacion 3: Comprobar si el token se encontro registrado en memoria
    if id_usuario is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="token invalido o sesion expirada"
        )
    
    # Se guarda el id del usuario en la informacion interna del request (variable "state"), 
    # por si algun controlador web necesita utilizar o validar quien esta haciendo originariamente
    # la peticion de crear o eliminar informacion.
    request.state.id_usuario = id_usuario
    
    # Devuelve el id_usuario al flujo principal que requirió validarlo
    return id_usuario
