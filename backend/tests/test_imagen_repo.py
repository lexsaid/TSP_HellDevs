from repositorios import imagenRepo
from modelos.modelos import Imagen


def test_actualizar_y_eliminar_imagen(seed_trabajo, fetch_scalar):
    # Arrange
    trabajo_id = seed_trabajo(nombre="ImgRepo")
    fetch_scalar(
        "INSERT INTO imagen (id_trabajo, imagen) VALUES (?, ?)",
        (trabajo_id, b"img"),
    )
    img_id = fetch_scalar("SELECT id_imagen FROM imagen ORDER BY id_imagen DESC LIMIT 1")
    imagen = Imagen(idImagen=img_id, idTrabajo=trabajo_id, imagen=b"img2")

    # Act
    ok_update = imagenRepo.actualizarImagen(
        "UPDATE imagen SET id_trabajo = ?, imagen = ? WHERE id_imagen = ?",
        imagen,
    )
    ok_delete = imagenRepo.eliminarImagen("DELETE FROM imagen WHERE id_imagen = ?", img_id)
    total = fetch_scalar("SELECT COUNT(*) FROM imagen WHERE id_imagen = ?", (img_id,))

    # Assert
    assert ok_update is True
    assert ok_delete is True
    assert total == 0
