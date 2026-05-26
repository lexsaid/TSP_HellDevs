# language: es
Característica: Gestión de Mensajería y Buzón
  Como usuario autenticado
  Quiero enviar mensajes sobre trabajos y ver mi buzón
  Para comunicarme con otros usuarios y mantener un registro de mis conversaciones

  Escenario: Ver el buzón vacío cuando no hay mensajes
    Dado que he iniciado sesión con el email "usuario_sin_mensajes@example.com"
    Cuando intento ver mi buzón
    Entonces el sistema debe responder con un código 200
    Y mi buzón debe estar vacío

  Escenario: Enviar un mensaje sobre un trabajo
    Dado que he iniciado sesión con el email "emisor@example.com"
    Y existe otro usuario con el email "receptor@example.com"
    Y existe un trabajo creado por el usuario "emisor@example.com"
    Cuando envío un mensaje con contenido "¿Aún disponible?" sobre el trabajo
    Entonces el sistema debe responder con un código 201
    Y el mensaje debe ser guardado correctamente

  Escenario: Ver el buzón con conversaciones activas
    Dado que he iniciado sesión con el email "usuario_principal@example.com"
    Y existe otro usuario con el email "otro_usuario@example.com"
    Y existe un trabajo creado por el usuario "usuario_principal@example.com"
    Y tengo mensajes no leídos de "otro_usuario@example.com" sobre ese trabajo
    Cuando intento ver mi buzón
    Entonces el sistema debe responder con un código 200
    Y debo ver la conversación con "otro_usuario@example.com" en mi buzón
    Y el título del trabajo debe aparecer en la conversación
