# language: es
Característica: Autenticación y Seguridad
  Como usuario del sistema
  Quiero iniciar sesión de forma segura
  Para poder acceder a las funciones protegidas de la aplicación

  Escenario: Inicio de sesión exitoso
    Dado que existe un usuario registrado con el email "exitoso@example.com" y contraseña "secreto123"
    Cuando intento iniciar sesión con el email "exitoso@example.com" y la contraseña "secreto123"
    Entonces el sistema debe responder con un código 200
    Y la respuesta debe contener un token válido de 64 caracteres

  Escenario: Intento de inicio de sesión con contraseña incorrecta
    Dado que existe un usuario registrado con el email "fallido@example.com" y contraseña "secreto123"
    Cuando intento iniciar sesión con el email "fallido@example.com" y la contraseña "erronea"
    Entonces el sistema debe responder con un código 401

  Escenario: Acceso denegado a ruta protegida con token inválido/ausente
    Dado que existe un usuario registrado con el email "protegido@example.com" y contraseña "secreto123"
    Cuando intento acceder a mi perfil sin proporcionar un token válido
    Entonces el sistema debe responder con un código 401
