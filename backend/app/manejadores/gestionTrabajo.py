from repositorios import trabajoRepo, imagenRepo
from modelos.modelos import Trabajo, Imagen
import base64

def crearTrabajo(trabajo: Trabajo) -> bool:
    consulta = "INSERT INTO trabajo (nombre, ubicacion, fecha_publicacion, monto, descripcion, id_animalLover_publicador, tipo_trabajo) VALUES (?, ?, ?, ?, ?, ?, ?)"
    id_trabajo = trabajoRepo.guardarTrabajo(consulta, trabajo)
    if id_trabajo > 0:
        if trabajo.imagenesBase64:
            for img_b64 in trabajo.imagenesBase64:
                try:
                    # Formato: "data:image/png;base64,iVBORw0KGgo..."
                    if "," in img_b64:
                        img_b64 = img_b64.split(",")[1]
                    img_bytes = base64.b64decode(img_b64)
                    imagen = Imagen(idTrabajo=id_trabajo, imagen=img_bytes)
                    consulta_img = "INSERT INTO imagen (id_trabajo, imagen) VALUES (?, ?)"
                    imagenRepo.guardarImagen(consulta_img, imagen)
                except Exception as e:
                    print(f"Error procesando imagen: {e}")
        return True
    return False

def obtenerTrabajo(idTrabajo: int) -> tuple[Trabajo, bool]:
    consulta = "SELECT * FROM trabajo WHERE id_trabajo = ?"
    return trabajoRepo.buscarIdTrabajo(consulta, idTrabajo)

def actualizarTrabajo(trabajo: Trabajo) -> bool:
    consulta = "UPDATE trabajo SET nombre = ?, ubicacion = ?, fecha_publicacion = ?, monto = ?, descripcion = ?, id_animalLover_publicador = ?, tipo_trabajo = ? WHERE id_trabajo = ?"
    exito = trabajoRepo.actualizarTrabajo(consulta, trabajo)
    if exito and trabajo.imagenesBase64 and len(trabajo.imagenesBase64) > 0:
        # Borrar imágenes anteriores y subir las nuevas
        imagenRepo.eliminarImagenesPorTrabajo(trabajo.idTrabajo)
        for img_b64 in trabajo.imagenesBase64:
            try:
                if "," in img_b64:
                    img_b64 = img_b64.split(",")[1]
                img_bytes = base64.b64decode(img_b64)
                imagen = Imagen(idTrabajo=trabajo.idTrabajo, imagen=img_bytes)
                consulta_img = "INSERT INTO imagen (id_trabajo, imagen) VALUES (?, ?)"
                imagenRepo.guardarImagen(consulta_img, imagen)
            except Exception as e:
                print(f"Error procesando imagen en actualización: {e}")
    return exito

def eliminarTrabajo(idTrabajo: int) -> bool:
    consulta = "DELETE FROM trabajo WHERE id_trabajo = ?"
    return trabajoRepo.eliminarTrabajo(consulta, idTrabajo)

def obtenerTodosLosTrabajos() -> tuple[list[Trabajo], bool]:
    consulta = "SELECT * FROM trabajo ORDER BY id_trabajo DESC"
    return trabajoRepo.buscarTodosTrabajos(consulta)
