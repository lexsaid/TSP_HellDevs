from repositorios.database import getDbConnection
from modelos.modelos import AnimalLover
import sqlite3

def guardarUsuario(consulta: str, usuario: AnimalLover) -> bool:
    try:
        conn = getDbConnection()
        cursor = conn.cursor()
        cursor.execute(consulta, (usuario.nombre, usuario.apellido, usuario.email, usuario.telefono, usuario.contrasena))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error al ejecutar la consulta en usuario: {e}")
        return False
    finally:
        if 'conn' in locals():
            conn.close()

def buscarIdUsuario(consulta: str, idUsuario: int) -> tuple[AnimalLover, bool]:
    try:
        conn = getDbConnection()
        cursor = conn.cursor()
        cursor.execute(consulta, (idUsuario,))
        row = cursor.fetchone()
        if row:
            usuario = AnimalLover(
                idAnimalLover=row['id_animalLover'],
                nombre=row['nombre'],
                apellido=row['apellido'],
                email=row['email'],
                telefono=row['telefono'],
                contraseña=row['contraseña'],
                token=row['token']
            )
            return usuario, True
        return None, False
    except sqlite3.Error as e:
        print(f"Error al buscar el usuario: {e}")
        return None, False
    finally:
        if 'conn' in locals():
            conn.close()

def buscarPorEmail(email: str) -> tuple[AnimalLover, bool]:
    try:
        conn = getDbConnection()
        cursor = conn.cursor()
        consulta = "SELECT * FROM animalLover WHERE email = ?"
        cursor.execute(consulta, (email,))
        row = cursor.fetchone()
        if row:
            usuario = AnimalLover(
                idAnimalLover=row['id_animalLover'],
                nombre=row['nombre'],
                apellido=row['apellido'],
                email=row['email'],
                telefono=row['telefono'],
                contraseña=row['contraseña'],
                token=row['token']
            )
            return usuario, True
        return None, False
    except sqlite3.Error as e:
        print(f"Error al buscar el usuario por email: {e}")
        return None, False
    finally:
        if 'conn' in locals():
            conn.close()

def actualizarUsuario(consulta: str, usuario: AnimalLover) -> bool:
    try:
        conn = getDbConnection()
        cursor = conn.cursor()
        cursor.execute(consulta, (usuario.nombre, usuario.apellido, usuario.email, usuario.telefono, usuario.contrasena, usuario.idAnimalLover))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error al actualizar la consulta en usuario: {e}")
        return False
    finally:
        if 'conn' in locals():
            conn.close()

def eliminarUsuario(consulta: str, idUsuario: int) -> bool:
    try:
        conn = getDbConnection()
        cursor = conn.cursor()
        cursor.execute(consulta, (idUsuario,))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error al eliminar la consulta en usuario: {e}")
        return False
    finally:
        if 'conn' in locals():
            conn.close()

def actualizarToken(idUsuario: int, token: str) -> bool:
    try:
        conn = getDbConnection()
        cursor = conn.cursor()
        consulta = "UPDATE animalLover SET token = ? WHERE id_animalLover = ?"
        cursor.execute(consulta, (token, idUsuario))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error al actualizar token: {e}")
        return False
    finally:
        if 'conn' in locals():
            conn.close()

def resetearTodosLosTokens() -> bool:
    try:
        conn = getDbConnection()
        cursor = conn.cursor()
        consulta = "UPDATE animalLover SET token = NULL"
        cursor.execute(consulta)
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error al resetear tokens: {e}")
        return False
    finally:
        if 'conn' in locals():
            conn.close()

def buscarPorToken(token: str) -> tuple[AnimalLover, bool]:
    try:
        conn = getDbConnection()
        cursor = conn.cursor()
        consulta = "SELECT * FROM animalLover WHERE token = ?"
        cursor.execute(consulta, (token,))
        row = cursor.fetchone()
        if row:
            usuario = AnimalLover(
                idAnimalLover=row['id_animalLover'],
                nombre=row['nombre'],
                apellido=row['apellido'],
                email=row['email'],
                telefono=row['telefono'],
                contraseña=row['contraseña'],
                token=row['token']
            )
            return usuario, True
        return None, False
    except sqlite3.Error as e:
        print(f"Error al buscar el usuario por token: {e}")
        return None, False
    finally:
        if 'conn' in locals():
            conn.close()
