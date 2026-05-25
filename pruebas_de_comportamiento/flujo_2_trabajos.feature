# language: es
Característica: Gestión de Trabajos
  Como usuario del sistema
  Quiero publicar y aceptar ofertas de trabajo
  Para poder interactuar con otras personas de la comunidad

  Escenario: Publicación exitosa de un trabajo por un usuario autenticado
    Dado que he iniciado sesión con el email "empleador@example.com"
    Cuando publico un nuevo trabajo con el título "Paseador de perros"
    Entonces el sistema debe responder con un código 201
    Y la respuesta debe indicar que el trabajo fue creado exitosamente

  Escenario: Búsqueda y visualización de ofertas de trabajo disponibles
    Dado que existe un trabajo publicado con el título "Cuidador fin de semana"
    Cuando solicito la lista de trabajos disponibles
    Entonces el sistema debe responder con un código 200
    Y la lista debe contener el trabajo "Cuidador fin de semana"

  Escenario: Aceptación de una oferta de trabajo modificando su estado
    Dado que he iniciado sesión con el email "trabajador@example.com"
    Y existe un trabajo disponible con el título "Limpieza de albergue"
    Cuando acepto el trabajo
    Entonces el sistema debe responder con un código 201
    Y el estado del trabajo aceptado debe quedar en "Pendiente"
