from repositorios.database import getDbConnection
from modelos.modelos import AnimalCalle, AdopcionDetalle, AnimalLoverDetalle
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
            INSERT INTO animalCalle (id_animal, vacunas)
            VALUES (?, ?)
        """
        cursor.execute(consulta_calle, (id_animal, adopcion.vacunas))
        
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
                ac.id_animalCalle, ac.vacunas,
                al.nombre as dueno_nombre, al.apellido, al.telefono, al.email
            FROM animalCalle ac
            INNER JOIN animal a ON ac.id_animal = a.id_animal
            INNER JOIN animalLover al ON a.id_animalLover = al.id_animalLover
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
                vacunas=row['vacunas']
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
