import base64
from fastapi import status


def _img_b64(data=b"img"):
    return "data:image/png;base64," + base64.b64encode(data).decode("ascii")


def test_login_y_crud_usuario(client, seed_user):
    # Arrange
    user = seed_user(email="login@example.com", telefono="1231231234", contrasena="pass123")
    login_payload = {"email": user.email, "contraseña": "pass123"}

    # Act
    ok_login = client.post("/login", json=login_payload)
    bad_login = client.post("/login", json={"email": user.email, "contraseña": "bad"})
    get_user = client.get("/animalLover", params={"id": user.idAnimalLover})
    put_user = client.put(
        "/animalLover",
        json={
            "idAnimalLover": user.idAnimalLover,
            "nombre": "Nuevo",
            "apellido": "Nombre",
            "email": "login@example.com",
            "telefono": "1231231234",
            "contraseña": "pass123",
        },
    )
    delete_user = client.delete("/animalLover", params={"id": user.idAnimalLover})

    # Assert
    assert ok_login.status_code == status.HTTP_200_OK
    assert "token" in ok_login.json()
    assert bad_login.status_code == status.HTTP_401_UNAUTHORIZED
    assert get_user.status_code == status.HTTP_200_OK
    assert put_user.status_code == status.HTTP_200_OK
    assert delete_user.status_code == status.HTTP_200_OK


def test_trabajo_routes_y_imagenes(client, seed_user):
    # Arrange
    user = seed_user(email="trabajo_api@example.com", telefono="3213213210")
    payload = {
        "nombre": "Trabajo",
        "ubicacion": "CDMX",
        "fechaPublicacion": "2024-01-01",
        "monto": 100.0,
        "descripcion": "Desc",
        "idAnimalLoverPublicador": user.idAnimalLover,
        "tipoTrabajo": "Servicio",
        "imagenesBase64": [_img_b64()],
    }

    # Act
    post_resp = client.post("/trabajo", json=payload)
    get_resp = client.get("/trabajo", params={"id": 1})
    list_resp = client.get("/trabajos")
    img_resp = client.get("/trabajo/1/imagen")
    info_resp = client.get("/trabajo/1/imagenes_info")
    idx_resp = client.get("/trabajo/1/imagen_index/0")
    idx_bad = client.get("/trabajo/1/imagen_index/2")
    put_resp = client.put(
        "/trabajo",
        json={**payload, "idTrabajo": 1, "imagenesBase64": [_img_b64(b"a"), _img_b64(b"b")], "nombre": "Trabajo2"},
    )
    delete_resp = client.delete("/trabajo", params={"id": 1})

    # Assert
    assert post_resp.status_code == status.HTTP_201_CREATED
    assert get_resp.status_code == status.HTTP_200_OK
    assert list_resp.status_code == status.HTTP_200_OK
    assert img_resp.status_code == status.HTTP_200_OK
    assert info_resp.json()["count"] == 1
    assert idx_resp.status_code == status.HTTP_200_OK
    assert idx_bad.status_code == status.HTTP_404_NOT_FOUND
    assert put_resp.status_code == status.HTTP_200_OK
    assert delete_resp.status_code == status.HTTP_200_OK


def test_trabajo_aceptado_routes(client, seed_user, seed_trabajo):
    # Arrange
    publicador = seed_user(email="pub@example.com", telefono="5550000001")
    trabajador = seed_user(email="trab@example.com", telefono="5550000002")
    trabajo_id = seed_trabajo(id_publicador=publicador.idAnimalLover)

    payload = {
        "idTrabajo": trabajo_id,
        "idAnimalLoverTrabajador": trabajador.idAnimalLover,
        "fechaAceptacion": "2024-01-01",
        "estadoTrabajo": "Pendiente",
    }

    # Act
    post_resp = client.post("/trabajo-aceptado", json=payload)
    list_resp = client.get("/trabajo-aceptado", params={"idAnimalLoverTrabajador": trabajador.idAnimalLover})
    put_resp = client.put("/trabajo-aceptado", json={**payload, "estadoTrabajo": "Terminado"})
    check_resp = client.get("/trabajo-aceptado/check", params={"idTrabajo": trabajo_id})
    completar = client.post("/trabajo-aceptado/completar", params={"idTrabajo": trabajo_id})
    delete_resp = client.delete(
        "/trabajo-aceptado",
        params={"idTrabajo": trabajo_id, "idAnimalLoverTrabajador": trabajador.idAnimalLover},
    )

    # Assert
    assert post_resp.status_code == status.HTTP_201_CREATED
    assert list_resp.status_code == status.HTTP_200_OK
    assert put_resp.status_code == status.HTTP_200_OK
    assert check_resp.status_code == status.HTTP_200_OK
    assert completar.status_code == status.HTTP_200_OK
    assert delete_resp.status_code == status.HTTP_200_OK


def test_mensajes_routes(client, seed_user, seed_trabajo, fetch_scalar):
    # Arrange
    emisor = seed_user(email="msg1@example.com", telefono="5550000101")
    receptor = seed_user(email="msg2@example.com", telefono="5550000102")
    trabajo_id = seed_trabajo(id_publicador=emisor.idAnimalLover)

    payload = {
        "idAnimalLoverEmisor": emisor.idAnimalLover,
        "idAnimalLoverReceptor": receptor.idAnimalLover,
        "idTrabajo": trabajo_id,
        "contenido": "Hola",
        "fechaMensaje": "2024-01-01",
    }

    # Act
    post_resp = client.post("/mensaje", json=payload)
    list_resp = client.get(
        "/mensaje",
        params={
            "idAnimalLover": emisor.idAnimalLover,
            "idOtroAnimalLover": receptor.idAnimalLover,
            "idTrabajo": trabajo_id,
        },
    )
    chats_resp = client.get("/chats", params={"idAnimalLover": emisor.idAnimalLover})
    nuevos_resp = client.get(
        "/mensajes/hay-nuevos",
        params={"idAnimalLover": receptor.idAnimalLover, "ultimoIdMensaje": 0},
    )

    mensaje_id = fetch_scalar("SELECT id_mensaje FROM mensajes ORDER BY id_mensaje DESC LIMIT 1")
    put_resp = client.put("/mensaje", params={"idMensaje": mensaje_id, "contenido": "Edit"})
    delete_resp = client.delete("/mensaje", params={"idMensaje": mensaje_id})

    # Assert
    assert post_resp.status_code == status.HTTP_201_CREATED
    assert list_resp.status_code == status.HTTP_200_OK
    assert chats_resp.status_code == status.HTTP_200_OK
    assert nuevos_resp.status_code == status.HTTP_200_OK
    assert put_resp.status_code == status.HTTP_200_OK
    assert delete_resp.status_code == status.HTTP_200_OK


def test_comunidad_routes_y_imagenes(client, seed_user, fetch_scalar):
    # Arrange
    user = seed_user(email="com1@example.com", telefono="5550000201")

    albergue_payload = {
        "idAnimalLover": user.idAnimalLover,
        "nombre": "Albergue",
        "ubicacion": "CDMX",
        "capacidad": 5,
        "preferencia": "Perros",
        "costoDiario": 20,
        "preRequisitos": "Req",
        "imagenesBase64": [_img_b64()],
    }

    mascota_payload = {
        "idAnimalLover": user.idAnimalLover,
        "nombre": "Perdido",
        "direccion": "CDMX",
        "tamanio": "M",
        "color": "Cafe",
        "discapacidad": "No",
        "tipoAnimal": "Perro",
        "edad": 3,
        "detallesAdicionales": "Det",
        "recompensa": "100",
        "imagenesBase64": [_img_b64()],
    }

    adopcion_payload = {
        "idAnimalLover": user.idAnimalLover,
        "nombre": "Adopcion",
        "direccion": "CDMX",
        "tamanio": "M",
        "color": "Negro",
        "discapacidad": "No",
        "tipoAnimal": "Gato",
        "edad": 2,
        "detallesAdicionales": "Det",
        "vacunas": "Basicas",
        "imagenesBase64": [_img_b64()],
    }

    # Act
    alb_post = client.post("/albergues", json=albergue_payload)
    alb_list = client.get("/albergues")
    alb_det = client.get("/albergues/detalle", params={"id_albergue": 1})
    alb_det_singular = client.get("/albergue", params={"id": 1})
    alb_put = client.put("/albergues", json={**albergue_payload, "idAlbergue": 1, "nombre": "Albergue2"})

    perd_post = client.post("/mascotas_perdidas", json=mascota_payload)
    perd_list = client.get("/mascotas_perdidas")
    perd_mis = client.get("/mascotas_perdidas/mis", params={"idAnimalLover": user.idAnimalLover})
    mascota_id = fetch_scalar("SELECT id_animal FROM animalPerdido ORDER BY id_animalPerdido DESC LIMIT 1")
    perd_det = client.get("/mascotas_perdidas/detalle", params={"id_animal": mascota_id})
    perd_put = client.put("/mascotas_perdidas", json={**mascota_payload, "idAnimal": mascota_id, "nombre": "Perdido2"})
    perd_local = client.post("/mascotas_perdidas/localizado", params={"id_animal": mascota_id})

    adop_post = client.post("/adopciones", json=adopcion_payload)
    adop_list = client.get("/adopciones")
    adop_mis = client.get("/adopciones/mis", params={"idAnimalLover": user.idAnimalLover})
    adopcion_id = fetch_scalar("SELECT id_animal FROM animalCalle ORDER BY id_animalCalle DESC LIMIT 1")
    adop_det = client.get("/adopciones/detalle", params={"id_animal": adopcion_id})
    adop_put = client.put("/adopciones", json={**adopcion_payload, "idAnimal": adopcion_id, "nombre": "Adopcion2"})
    adop_mark = client.post("/adopciones/adoptado", params={"id_animal": adopcion_id})

    img_animal = client.get(f"/animal/{mascota_id}/imagen")
    img_animal_info = client.get(f"/animal/{mascota_id}/imagenes_info")
    img_animal_idx = client.get(f"/animal/{mascota_id}/imagen_index/0")

    img_alb = client.get("/albergue/1/imagen")
    img_alb_info = client.get("/albergue/1/imagenes_info")
    img_alb_idx = client.get("/albergue/1/imagen_index/0")

    perd_del = client.delete("/mascotas_perdidas", params={"id_animal": mascota_id})
    adop_del = client.delete("/adopciones", params={"id_animal": adopcion_id})
    alb_del = client.delete("/albergues", params={"id_albergue": 1})

    # Assert
    assert alb_post.status_code == status.HTTP_201_CREATED
    assert alb_list.status_code == status.HTTP_200_OK
    assert alb_det.status_code == status.HTTP_200_OK
    assert alb_det_singular.status_code == status.HTTP_200_OK
    assert alb_put.status_code == status.HTTP_200_OK

    assert perd_post.status_code == status.HTTP_201_CREATED
    assert perd_list.status_code == status.HTTP_200_OK
    assert perd_mis.status_code == status.HTTP_200_OK
    assert perd_det.status_code == status.HTTP_200_OK
    assert perd_put.status_code == status.HTTP_200_OK
    assert perd_local.status_code == status.HTTP_200_OK

    assert adop_post.status_code == status.HTTP_201_CREATED
    assert adop_list.status_code == status.HTTP_200_OK
    assert adop_mis.status_code == status.HTTP_200_OK
    assert adop_det.status_code == status.HTTP_200_OK
    assert adop_put.status_code == status.HTTP_200_OK
    assert adop_mark.status_code == status.HTTP_200_OK

    assert img_animal.status_code == status.HTTP_200_OK
    assert img_animal_info.status_code == status.HTTP_200_OK
    assert img_animal_idx.status_code == status.HTTP_200_OK

    assert img_alb.status_code == status.HTTP_200_OK
    assert img_alb_info.status_code == status.HTTP_200_OK
    assert img_alb_idx.status_code == status.HTTP_200_OK

    assert perd_del.status_code == status.HTTP_200_OK
    assert adop_del.status_code == status.HTTP_200_OK
    assert alb_del.status_code == status.HTTP_200_OK
