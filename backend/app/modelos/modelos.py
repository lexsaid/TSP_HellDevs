from pydantic import BaseModel, Field
from typing import Optional

class AnimalLoverLogin(BaseModel):
    email: str
    contrasena: str = Field(alias="contraseña")

class AnimalLover(BaseModel):
    idAnimalLover: Optional[int] = None
    nombre: str
    apellido: str
    email: str
    telefono: str
    contrasena: str = Field(alias="contraseña")
    token: Optional[str] = None

class Trabajo(BaseModel):
    idTrabajo: Optional[int] = None
    nombre: str
    ubicacion: str
    fechaPublicacion: str
    monto: float
    descripcion: str
    idAnimalLoverPublicador: int
    tipoTrabajo: str
    imagenesBase64: Optional[list[str]] = []

class TrabajoAceptado(BaseModel):
    idTrabajo: int
    idAnimalLoverTrabajador: int
    fechaAceptacion: str
    estadoTrabajo: str

class Mensaje(BaseModel):
    idMensaje: Optional[int] = None
    idAnimalLoverEmisor: int
    idAnimalLoverReceptor: int
    idTrabajo: int
    contenido: str
    fechaMensaje: str

class Imagen(BaseModel):
    idImagen: Optional[int] = None
    idTrabajo: int
    imagen: bytes
