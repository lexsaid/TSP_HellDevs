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

class Animal(BaseModel):
    idAnimal: Optional[int] = None
    idAnimalLover: int
    nombre: str
    direccion: str
    tamanio: str
    color: str
    discapacidad: str
    tipoAnimal: str
    edad: int
    detallesAdicionales: Optional[str] = None
    imagenesBase64: Optional[list[str]] = []

class AnimalPerdido(Animal):
    idAnimalPerdido: Optional[int] = None
    recompensa: str
    estado: Optional[str] = "Activo"

class AnimalCalle(Animal):
    idAnimalCalle: Optional[int] = None
    vacunas: str
    estado: Optional[str] = "Activo"

class Albergue(BaseModel):
    idAlbergue: Optional[int] = None
    idAnimalLover: int
    nombre: str
    ubicacion: str
    capacidad: int
    preferencia: str
    costoDiario: int
    preRequisitos: str
    imagenesBase64: Optional[list[str]] = []

class AnimalLoverDetalle(BaseModel):
    idAnimalLover: int
    nombre: str
    apellido: str
    telefono: str
    email: str

class MascotaPerdidaDetalle(BaseModel):
    mascotaPerdida: AnimalPerdido
    dueño: AnimalLoverDetalle
    
class AdopcionDetalle(BaseModel):
    adopcion: AnimalCalle
    publicador: AnimalLoverDetalle

class AlbergueDetalle(BaseModel):
    albergue: Albergue
    dueño: AnimalLoverDetalle
