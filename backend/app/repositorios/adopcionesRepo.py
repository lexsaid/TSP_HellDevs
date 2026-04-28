from repositorios.database import getDbConnection
from modelos.modelos import AnimalCalle, AdopcionDetalle, AnimalLoverDetalle
from typing import Optional
import sqlite3

def guardarAdopcion(adopcion: AnimalCalle) -> int:
    try:
        conn = getDbConnection()
        cursor = conn.cursor()
        
        # Insertar primero en animal
        consulta_animal = """
            INSERT INTO animal (id_animalLover, nombre, direccion, tamanio, color, discapacidad, tipo_animal, edad, detalles_adicionales)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        cursor.execute(consulta_animal, (
            adopcion.idAnimalLover,
            adopcion.nombre,
            adopcion.direccion,
            adopcion.tamanio,
            adopcion.color,
            adopcion.discapacidad,
            adopcion.tipoAnimal,
            adopcion.edad,
            adopcion.detallesAdicionales
        ))
        
        id_animal = cursor.lastrowid
        
        # Luego insertar en animalCalle
        consulta_calle = """
            INSERT INTO animalCalle (id_animal, vacunas, estado)
            VALUES (?, ?, ?)
        """
        cursor.execute(consulta_calle, (id_animal, adopcion.vacunas, adopcion.estado or "Activo"))
        
        conn.commit()
        return id_animal
    except sqlite3.Error as e:
        if 'conn' in locals():
            conn.rollback()
        print(f"Error al guardar Adopción: {e}")
        return -1
    finally:
        if 'conn' in locals():
            conn.close()

def buscarTodasAdopciones() -> tuple[list[AdopcionDetalle], bool]:
    try:
        conn = getDbConnection()
        cursor = conn.cursor()
        consulta = """
            SELECT 
                a.id_animal, a.id_animalLover, a.nombre as animal_nombre, a.direccion, a.tamanio, a.color, 
                a.discapacidad, a.tipo_animal, a.edad, a.detalles_adicionales,
                ac.id_animalCalle, ac.vacunas, ac.estado,
                al.nombre as dueno_nombre, al.apellido, al.telefono, al.email
            FROM animalCalle ac
            INNER JOIN animal a ON ac.id_animal = a.id_animal
            INNER JOIN animalLover al ON a.id_animalLover = al.id_animalLover
            WHERE ac.estado = 'Activo'
            ORDER BY ac.id_animalCalle DESC
        """
        cursor.execute(consulta)
        rows = cursor.fetchall()
        detalles = []
        for row in rows:
            animal_calle = AnimalCalle(
                idAnimal=row['id_animal'],
                idAnimalLover=row['id_animalLover'],
                nombre=row['animal_nombre'],
                direccion=row['direccion'],
                tamanio=row['tamanio'],
                color=row['color'],
                discapacidad=row['discapacidad'],
                tipoAnimal=row['tipo_animal'],
                edad=row['edad'],
                detallesAdicionales=row['detalles_adicionales'],
                idAnimalCalle=row['id_animalCalle'],
                vacunas=row['vacunas'],
                estado=row['estado']
            )
            publicador = AnimalLoverDetalle(
                idAnimalLover=row['id_animalLover'],
                nombre=row['dueno_nombre'],
                apellido=row['apellido'],
                telefono=row['telefono'],
                email=row['email']
            )
            detalles.append(AdopcionDetalle(adopcion=animal_calle, publicador=publicador))
        return detalles, True
    except sqlite3.Error as e:
        print(f"Error al buscar todas las adopciones: {e}")
        return [], False
    finally:
        if 'conn' in locals():
            conn.close()


def buscarAdopcionesPorUsuario(id_animalLover: int) -> tuple[list[AdopcionDetalle], bool]:
    try:
        conn = getDbConnection()
        cursor = conn.cursor()
        consulta = """
            SELECT 
                a.id_animal, a.id_animalLover, a.nombre as animal_nombre, a.direccion, a.tamanio, a.color, 
                a.discapacidad, a.tipo_animal, a.edad, a.detalles_adicionales,
                ac.id_animalCalle, ac.vacunas, ac.estado,
                al.nombre as dueno_nombre, al.apellido, al.telefono, al.email
            FROM animalCalle ac
            INNER JOIN animal a ON ac.id_animal = a.id_animal
            INNER JOIN animalLover al ON a.id_animalLover = al.id_animalLover
            WHERE a.id_animalLover = ?
            ORDER BY ac.id_animalCalle DESC
        """
        cursor.execute(consulta, (id_animalLover,))
        rows = cursor.fetchall()
        detalles = []
        for row in rows:
            animal_calle = AnimalCalle(
                idAnimal=row['id_animal'],
                idAnimalLover=row['id_animalLover'],
                nombre=row['animal_nombre'],
                direccion=row['direccion'],
                tamanio=row['tamanio'],
                color=row['color'],
                discapacidad=row['discapacidad'],
                tipoAnimal=row['tipo_animal'],
                edad=row['edad'],
                detallesAdicionales=row['detalles_adicionales'],
                idAnimalCalle=row['id_animalCalle'],
                vacunas=row['vacunas'],
                estado=row['estado']
            )
            publicador = AnimalLoverDetalle(
                idAnimalLover=row['id_animalLover'],
                nombre=row['dueno_nombre'],
                apellido=row['apellido'],
                telefono=row['telefono'],
                email=row['email']
            )
            detalles.append(AdopcionDetalle(adopcion=animal_calle, publicador=publicador))
        return detalles, True
    except sqlite3.Error as e:
        print(f"Error al buscar adopciones por usuario: {e}")
        return [], False
    finally:
        if 'conn' in locals():
            conn.close()


def buscarAdopcionPorId(id_animal: int) -> tuple[Optional[AdopcionDetalle], bool]:
    try:
        conn = getDbConnection()
        cursor = conn.cursor()
        consulta = """
            SELECT 
                a.id_animal, a.id_animalLover, a.nombre as animal_nombre, a.direccion, a.tamanio, a.color, 
                a.discapacidad, a.tipo_animal, a.edad, a.detalles_adicionales,
                ac.id_animalCalle, ac.vacunas, ac.estado,
                al.nombre as dueno_nombre, al.apellido, al.telefono, al.email
            FROM animalCalle ac
            INNER JOIN animal a ON ac.id_animal = a.id_animal
            INNER JOIN animalLover al ON a.id_animalLover = al.id_animalLover
            WHERE a.id_animal = ?
        """
        cursor.execute(consulta, (id_animal,))
        row = cursor.fetchone()
        if not row:
            return None, False

        animal_calle = AnimalCalle(
            idAnimal=row['id_animal'],
            idAnimalLover=row['id_animalLover'],
            nombre=row['animal_nombre'],
            direccion=row['direccion'],
            tamanio=row['tamanio'],
            color=row['color'],
            discapacidad=row['discapacidad'],
            tipoAnimal=row['tipo_animal'],
            edad=row['edad'],
            detallesAdicionales=row['detalles_adicionales'],
            idAnimalCalle=row['id_animalCalle'],
            vacunas=row['vacunas'],
            estado=row['estado']
        )
        publicador = AnimalLoverDetalle(
            idAnimalLover=row['id_animalLover'],
            nombre=row['dueno_nombre'],
            apellido=row['apellido'],
            telefono=row['telefono'],
            email=row['email']
        )
        return AdopcionDetalle(adopcion=animal_calle, publicador=publicador), True
    except sqlite3.Error as e:
        print(f"Error al buscar adopcion por id: {e}")
        return None, False
    finally:
        if 'conn' in locals():
            conn.close()


def actualizarAdopcion(adopcion: AnimalCalle) -> bool:
    try:
        conn = getDbConnection()
        cursor = conn.cursor()

        consulta_animal = """
            UPDATE animal
            SET nombre = ?, direccion = ?, tamanio = ?, color = ?, discapacidad = ?, tipo_animal = ?, edad = ?, detalles_adicionales = ?
            WHERE id_animal = ?
        """
        cursor.execute(consulta_animal, (
            adopcion.nombre,
            adopcion.direccion,
            adopcion.tamanio,
            adopcion.color,
            adopcion.discapacidad,
            adopcion.tipoAnimal,
            adopcion.edad,
            adopcion.detallesAdicionales,
            adopcion.idAnimal
        ))

        consulta_calle = """
            UPDATE animalCalle
            SET vacunas = ?, estado = ?
            WHERE id_animal = ?
        """
        cursor.execute(consulta_calle, (
            adopcion.vacunas,
            adopcion.estado or "Activo",
            adopcion.idAnimal
        ))

        conn.commit()
        return cursor.rowcount > 0
    except sqlite3.Error as e:
        if 'conn' in locals():
            conn.rollback()
        print(f"Error al actualizar adopcion: {e}")
        return False
    finally:
        if 'conn' in locals():
            conn.close()


def actualizarEstadoAdopcion(id_animal: int, estado: str) -> bool:
    try:
        conn = getDbConnection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE animalCalle SET estado = ? WHERE id_animal = ?",
            (estado, id_animal)
        )
        conn.commit()
        return cursor.rowcount > 0
    except sqlite3.Error as e:
        if 'conn' in locals():
            conn.rollback()
        print(f"Error al actualizar estado de adopcion: {e}")
        return False
    finally:
        if 'conn' in locals():
            conn.close()


def eliminarAdopcion(id_animal: int) -> bool:
    try:
        conn = getDbConnection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM imagen_animal WHERE id_animal = ?", (id_animal,))
        cursor.execute("DELETE FROM animalCalle WHERE id_animal = ?", (id_animal,))
        cursor.execute("DELETE FROM animal WHERE id_animal = ?", (id_animal,))
        conn.commit()
        return True
    except sqlite3.Error as e:
        if 'conn' in locals():
            conn.rollback()
        print(f"Error al eliminar adopcion: {e}")
        return False
    finally:
        if 'conn' in locals():
            conn.close()
