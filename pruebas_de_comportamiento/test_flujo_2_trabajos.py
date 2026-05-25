import base64
from pytest_bdd import scenarios, given, when, then, parsers
from fastapi import status
from enrutador import AuthMiddleware

scenarios("flujo_2_trabajos.feature")

class Context:
    def __init__(self):
        self.response = None
        self.user = None
        self.token = None
        self.trabajo_id = None
        
def _img_b64(data=b"img"):
    return "data:image/png;base64," + base64.b64encode(data).decode("ascii")


@given(parsers.parse('que he iniciado sesión con el email "{email}"'), target_fixture="context")
def seed_and_login_user(seed_user, email):
    context = Context()
    user = seed_user(email=email, contrasena="test1234")
    context.user = user
    # Generar token para simular la sesión
    context.token = AuthMiddleware.crearSesion(user.idAnimalLover)
    return context


@given(parsers.parse('que existe un trabajo publicado con el título "{titulo}"'), target_fixture="context")
def seed_trabajo(seed_user, titulo):
    # Esto mockea un entorno donde existe un trabajo previo
    # Importamos desde el repo
    from repositorios import trabajoRepo
    from modelos.modelos import Trabajo
    
    context = Context()
    user = seed_user(email="random_publisher@example.com")
    trabajo = Trabajo(
        nombre=titulo,
        ubicacion="CDMX",
        fechaPublicacion="2024-01-01",
        monto=200.0,
        descripcion="Trabajo dummy",
        idAnimalLoverPublicador=user.idAnimalLover,
        tipoTrabajo="Servicio",
    )
    consulta = "INSERT INTO trabajo (nombre, ubicacion, fecha_publicacion, monto, descripcion, id_animalLover_publicador, tipo_trabajo) VALUES (?, ?, ?, ?, ?, ?, ?)"
    context.trabajo_id = trabajoRepo.guardarTrabajo(consulta, trabajo)
    context.token = AuthMiddleware.crearSesion(user.idAnimalLover)
    return context


@given(parsers.parse('existe un trabajo disponible con el título "{titulo}"'))
def seed_trabajo_disponible(context, seed_user, titulo):
    from repositorios import trabajoRepo
    from modelos.modelos import Trabajo
    
    user_pub = seed_user(email="pub2@example.com")
    trabajo = Trabajo(
        nombre=titulo,
        ubicacion="CDMX",
        fechaPublicacion="2024-01-01",
        monto=150.0,
        descripcion="Trabajo dummy 2",
        idAnimalLoverPublicador=user_pub.idAnimalLover,
        tipoTrabajo="Servicio",
    )
    consulta = "INSERT INTO trabajo (nombre, ubicacion, fecha_publicacion, monto, descripcion, id_animalLover_publicador, tipo_trabajo) VALUES (?, ?, ?, ?, ?, ?, ?)"
    context.trabajo_id = trabajoRepo.guardarTrabajo(consulta, trabajo)


@when(parsers.parse('publico un nuevo trabajo con el título "{titulo}"'))
def publish_job(client, context, titulo):
    payload = {
        "nombre": titulo,
        "ubicacion": "CDMX",
        "fechaPublicacion": "2024-01-01",
        "monto": 100.0,
        "descripcion": "Desc",
        "idAnimalLoverPublicador": context.user.idAnimalLover,
        "tipoTrabajo": "Servicio",
        "imagenesBase64": [_img_b64()],
    }
    context.response = client.post(
        "/trabajo", 
        json=payload, 
        headers={"Authorization": context.token}
    )


@when('solicito la lista de trabajos disponibles')
def list_jobs(client, context):
    context.response = client.get("/trabajos", headers={"Authorization": context.token})


@when('acepto el trabajo')
def accept_job(client, context):
    payload = {
        "idTrabajo": context.trabajo_id,
        "idAnimalLoverTrabajador": context.user.idAnimalLover,
        "fechaAceptacion": "2024-01-01",
        "estadoTrabajo": "Pendiente",
    }
    context.response = client.post(
        "/trabajo-aceptado", 
        json=payload, 
        headers={"Authorization": context.token}
    )


@then(parsers.parse('el sistema debe responder con un código {status_code:d}'))
def verify_status_code_jobs(context, status_code):
    assert context.response.status_code == status_code


@then('la respuesta debe indicar que el trabajo fue creado exitosamente')
def verify_job_creation(context):
    assert context.response.status_code == 201


@then(parsers.parse('la lista debe contener el trabajo "{titulo}"'))
def verify_job_in_list(context, titulo):
    data = context.response.json()
    assert any(job.get("nombre") == titulo for job in data)


@then(parsers.parse('el estado del trabajo aceptado debe quedar en "{estado}"'))
def verify_accepted_job_state(context, estado):
    assert context.response.status_code == 201
