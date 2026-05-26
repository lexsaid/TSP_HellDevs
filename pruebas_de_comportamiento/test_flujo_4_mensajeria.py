import base64
from pytest_bdd import scenarios, given, when, then, parsers
from fastapi import status
from enrutador import AuthMiddleware
from manejadores import manejadorMensajes, manejadorTrabajo
from modelos.modelos import Mensaje

scenarios("flujo_4_mensajeria.feature")


class Context:
    def __init__(self):
        self.response = None
        self.user = None
        self.otro_usuario = None
        self.token = None
        self.trabajo_id = None
        self.mensaje = None


def _img_b64(data=b"img"):
    return "data:image/png;base64," + base64.b64encode(data).decode("ascii")


@given(parsers.parse('que he iniciado sesión con el email "{email}"'), target_fixture="context")
def login_usuario(seed_user, email):
    context = Context()
    user = seed_user(email=email, contrasena="test1234")
    context.user = user
    context.token = AuthMiddleware.crearSesion(user.idAnimalLover)
    return context


@given(parsers.parse('existe otro usuario con el email "{email}"'))
def create_otro_usuario(seed_user, context, email):
    context.otro_usuario = seed_user(email=email, contrasena="test1234")


@given(parsers.parse('existe un trabajo creado por el usuario "{email}"'))
def create_trabajo(seed_trabajo, context, email):
    # Si el trabajo es creado por el usuario autenticado
    if email == context.user.email:
        usuario_creador = context.user
    else:
        # Buscar el usuario por email
        usuarios = [context.user]
        if hasattr(context, 'otro_usuario') and context.otro_usuario:
            usuarios.append(context.otro_usuario)
        usuario_creador = next((u for u in usuarios if u.email == email), context.user)
    
    context.trabajo_id = seed_trabajo(
        nombre="Trabajo de Prueba",
        id_publicador=usuario_creador.idAnimalLover
    )


@given(parsers.parse('tengo mensajes no leídos de "{email}" sobre ese trabajo'))
def crear_mensajes_previos(context, email):
    # Usar el otro_usuario que ya fue creado
    if context.otro_usuario and context.otro_usuario.email == email:
        otro_user = context.otro_usuario
    else:
        # Si no coincide, ignorar
        return
    
    # Crear mensaje del otro usuario hacia el usuario autenticado
    mensaje = Mensaje(
        idAnimalLoverEmisor=otro_user.idAnimalLover,
        idAnimalLoverReceptor=context.user.idAnimalLover,
        idTrabajo=context.trabajo_id,
        contenido="Hola, ¿puedo ayudarte con este trabajo?",
        fechaMensaje="2024-01-01 10:30",
    )
    manejadorMensajes.guardarMensaje(mensaje)


@when('intento ver mi buzón')
def obtener_buzón(client, context):
    context.response = client.get(
        "/chats",
        params={"idAnimalLover": context.user.idAnimalLover},
        headers={"Authorization": context.token}
    )


@when(parsers.parse('envío un mensaje con contenido "{contenido}" sobre el trabajo'))
def enviar_mensaje(client, context, contenido):
    mensaje_data = {
        "idAnimalLoverEmisor": context.user.idAnimalLover,
        "idAnimalLoverReceptor": context.otro_usuario.idAnimalLover,
        "idTrabajo": context.trabajo_id,
        "contenido": contenido,
        "fechaMensaje": "2024-01-01 10:00",
    }
    context.response = client.post(
        "/mensaje",
        json=mensaje_data,
        headers={"Authorization": context.token}
    )


@then(parsers.parse('el sistema debe responder con un código {status_code:d}'))
def verify_status_code(context, status_code):
    assert context.response.status_code == status_code


@then('mi buzón debe estar vacío')
def verify_empty_inbox(context):
    data = context.response.json()
    assert isinstance(data, list)
    assert len(data) == 0


@then('el mensaje debe ser guardado correctamente')
def verify_mensaje_guardado(context):
    data = context.response.json()
    assert "mensaje" in data


@then(parsers.parse('debo ver la conversación con "{email}" en mi buzón'))
def verify_conversacion_en_buzón(context, email):
    data = context.response.json()
    assert isinstance(data, list)
    assert len(data) > 0, "El buzón debe tener al menos una conversación"
    
    # Verificar que hay al menos una conversación con el trabajo que creamos
    conversacion_encontrada = False
    for chat in data:
        # Verificar que sea del trabajo esperado
        if chat.get("idTrabajo") == context.trabajo_id:
            conversacion_encontrada = True
            # Verificar que el otro usuario esté en la conversación
            nombre_usuario = chat.get("nombreUsuario", "").lower()
            assert nombre_usuario, f"La conversación debe tener nombreUsuario"
            break
    
    assert conversacion_encontrada, f"No se encontró conversación sobre el trabajo {context.trabajo_id} en el buzón"


@then('el título del trabajo debe aparecer en la conversación')
def verify_titulo_trabajo_en_conversacion(context):
    data = context.response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    
    # Verificar que al menos una conversación tenga el título del trabajo
    for chat in data:
        if chat.get("idTrabajo") == context.trabajo_id:
            assert chat.get("tituloTrabajo") is not None
            assert chat["tituloTrabajo"] == "Trabajo de Prueba"
            return
    
    raise AssertionError("No se encontró el título del trabajo en ninguna conversación")
