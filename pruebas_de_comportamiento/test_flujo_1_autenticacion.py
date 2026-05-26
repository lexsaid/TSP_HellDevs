from pytest_bdd import scenarios, given, when, then, parsers
from fastapi import status
from manejadores import manejadorUsuario

# Cargar los escenarios del feature
scenarios("flujo_1_autenticacion.feature")

# Estado compartido entre steps
class Context:
    def __init__(self):
        self.response = None
        self.user = None


@given(parsers.parse('que existe un usuario registrado con el email "{email}" y contraseña "{contrasena}"'), target_fixture="context")
def seed_test_user(seed_user, email, contrasena):
    context = Context()
    context.user = seed_user(email=email, contrasena=contrasena)
    return context


@when(parsers.parse('intento iniciar sesión con el email "{email}" y la contraseña "{contrasena}"'))
def attempt_login(client, context, email, contrasena):
    payload = {"email": email, "contraseña": contrasena}
    context.response = client.post("/login", json=payload)


@when('intento acceder a mi perfil sin proporcionar un token válido')
def attempt_access_profile_without_token(client, context):
    context.response = client.post("/trabajo", json={}, headers={"Authorization": "bad-token"})


@then(parsers.parse('el sistema debe responder con un código {status_code:d}'))
def verify_status_code(context, status_code):
    assert context.response.status_code == status_code


@then('la respuesta debe contener un token válido de 64 caracteres')
def verify_token_in_response(context):
    data = context.response.json()
    assert "token" in data
    token = data["token"]
    assert len(token) == 64
