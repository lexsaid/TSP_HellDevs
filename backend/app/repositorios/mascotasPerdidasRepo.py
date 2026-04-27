from repositorios.database import getDbConnection
from modelos.modelos import AnimalPerdido, MascotaPerdidaDetalle, AnimalLoverDetalle
import sqlite3

def guardarMascotaPerdida(mascota: AnimalPerdido) -> int:
    try:
        conn = getDbConnection()
        cursor = conn.cursor()
        
        # Insertar primero en animal
        consulta_animal = """
            INSERT INTO animal (id_animalLover, nombre, direccion, tamanio, color, discapacidad, tipo_animal, edad, detalles_adicionales)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        cursor.execute(consulta_animal, (
            mascota.idAnimalLover,
            mascota.nombre,
            mascota.direccion,
            mascota.tamanio,
            mascota.color,
            mascota.discapacidad,
            mascota.tipoAnimal,
            mascota.edad,
            mascota.detallesAdicionales
        ))
        
        id_animal = cursor.lastrowid
        
        # Luego insertar en animalPerdido
        consulta_perdido = """
            INSERT INTO animalPerdido (id_animal, recompensa)
            VALUES (?, ?)
        """
        cursor.execute(consulta_perdido, (id_animal, mascota.recompensa))
        
        conn.commit()
        return id_animal
    except sqlite3.Error as e:
        if 'conn' in locals():
            conn.rollback()
        print(f"Error al guardar Mascota Perdida: {e}")
        return -1
    finally:
        if 'conn' in locals():
            conn.close()

def buscarTodasMascotasPerdidas() -> tuple[list[MascotaPerdidaDetalle], bool]:
    try:
        conn = getDbConnection()
        cursor = conn.cursor()
        consulta = """
            SELECT 
                a.id_animal, a.id_animalLover, a.nombre as animal_nombre, a.direccion, a.tamanio, a.color, 
                a.discapacidad, a.tipo_animal, a.edad, a.detalles_adicionales,
                ap.id_animalPerdido, ap.recompensa,
                al.nombre as dueno_nombre, al.apellido, al.telefono, al.email
            FROM animalPerdido ap
            INNER JOIN animal a ON ap.id_animal = a.id_animal
            INNER JOIN animalLover al ON a.id_animalLover = al.id_animalLover
            ORDER BY ap.id_animalPerdido DESC
        """
        cursor.execute(consulta)
        rows = cursor.fetchall()
        detalles = []
        for row in rows:
            animal_perdido = AnimalPerdido(
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
                idAnimalPerdido=row['id_animalPerdido'],
                recompensa=str(row['recompensa'])
            )
            dueno = AnimalLoverDetalle(
                idAnimalLover=row['id_animalLover'],
                nombre=row['dueno_nombre'],
                apellido=row['apellido'],
                telefono=row['telefono'],
                email=row['email']
            )
            detalles.append(MascotaPerdidaDetalle(mascotaPerdida=animal_perdido, dueño=dueno))
        return detalles, True
    except sqlite3.Error as e:
        print(f"Error al buscar todas las mascotas perdidas: {e}")
        return [], False
    finally:
        if 'conn' in locals():
            conn.close()
