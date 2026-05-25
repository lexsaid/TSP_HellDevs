# language: es
Característica: Gestión de Adopciones y Animales
  Como amante de los animales
  Quiero poder registrar albergues y publicar mascotas perdidas o en adopción
  Para contribuir a la comunidad y ayudar a los animales

  Escenario: Registro exitoso de un albergue por un idAnimalLover autenticado
    Dado que he iniciado sesión con el email "albergue_admin@example.com"
    Cuando registro un nuevo albergue con el nombre "Refugio Esperanza"
    Entonces el sistema debe responder con un código 201
    Y la respuesta debe indicar que el albergue fue creado exitosamente

  Escenario: Publicación de una mascota en adopción vinculada al albergue
    Dado que he iniciado sesión con el email "albergue_admin@example.com"
    Cuando publico un animal en adopción de nombre "Firulais" y tipo "Perro"
    Entonces el sistema debe responder con un código 201
    Y la respuesta debe confirmar la publicación de la adopción

  Escenario: Reporte de una mascota perdida con sus datos correspondientes
    Dado que he iniciado sesión con el email "dueño_triste@example.com"
    Cuando reporto a mi mascota perdida de nombre "Michi" y tipo "Gato"
    Entonces el sistema debe responder con un código 201
    Y la respuesta debe confirmar el reporte de la mascota perdida
