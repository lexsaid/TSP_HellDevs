import base64
from pytest_bdd import scenarios, given, when, then, parsers
from fastapi import status
from enrutador import AuthMiddleware

scenarios("flujo_3_adopciones.feature")

class Context:
    def __init__(self):
        self.response = None
        self.user = None
        self.token = None
        
def _img_b64(data=b"img"):
    return "data:image/png;base64," + base64.b64encode(data).decode("ascii")


@given(parsers.parse('que he iniciado sesión con el email "{email}"'), target_fixture="context")
def seed_and_login_user(seed_user, email):
    context = Context()
    user = seed_user(email=email, contrasena="test1234")
    context.user = user
    context.token = AuthMiddleware.crearSesion(user.idAnimalLover)
    return context


@when(parsers.parse('registro un nuevo albergue con el nombre "{nombre}"'))
def register_albergue(client, context, nombre):
    payload = {
        "idAnimalLover": context.user.idAnimalLover,
        "nombre": nombre,
        "ubicacion": "CDMX",
        "capacidad": 5,
        "preferencia": "Perros",
        "costoDiario": 20,
        "preRequisitos": "Amor",
        "imagenesBase64": [_img_b64()],
    }
    context.response = client.post(
        "/albergues", 
        json=payload, 
        headers={"Authorization": context.token}
    )


@when(parsers.parse('publico un animal en adopción de nombre "{nombre}" y tipo "{tipo}"'))
def publish_adoption(client, context, nombre, tipo):
    payload = {
        "idAnimalLover": context.user.idAnimalLover,
        "nombre": nombre,
        "direccion": "CDMX",
        "tamanio": "M",
        "color": "Negro",
        "discapacidad": "No",
        "tipoAnimal": tipo,
        "edad": 2,
        "detallesAdicionales": "Ninguno",
        "vacunas": "Basicas",
        "imagenesBase64": [_img_b64()],
    }
    context.response = client.post(
        "/adopciones", 
        json=payload, 
        headers={"Authorization": context.token}
    )


@when(parsers.parse('reporto a mi mascota perdida de nombre "{nombre}" y tipo "{tipo}"'))
def report_lost_pet(client, context, nombre, tipo):
    payload = {
        "idAnimalLover": context.user.idAnimalLover,
        "nombre": nombre,
        "direccion": "CDMX",
        "tamanio": "M",
        "color": "Cafe",
        "discapacidad": "No",
        "tipoAnimal": tipo,
        "edad": 3,
        "detallesAdicionales": "Tiene collar azul",
        "recompensa": "100",
        "imagenesBase64": [_img_b64()],
    }
    context.response = client.post(
        "/mascotas_perdidas", 
        json=payload, 
        headers={"Authorization": context.token}
    )


@then(parsers.parse('el sistema debe responder con un código {status_code:d}'))
def verify_status_code_adoptions(context, status_code):
    assert context.response.status_code == status_code


@then('la respuesta debe indicar que el albergue fue creado exitosamente')
def verify_albergue_creation(context):
    assert context.response.status_code == 201


@then('la respuesta debe confirmar la publicación de la adopción')
def verify_adoption_creation(context):
    assert context.response.status_code == 201


@then('la respuesta debe confirmar el reporte de la mascota perdida')
def verify_lost_pet_creation(context):
    assert context.response.status_code == 201
