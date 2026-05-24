import random
from locust import HttpUser, task, between

class TSP_HellDevs_User(HttpUser):
    # Tiempo de espera entre tareas (1 a 5 segundos)
    wait_time = between(1, 5)

    def on_start(self):
        """Inicialización que corre una vez por usuario virtual."""
        # Se asume que en el sistema real o en la DB de pruebas habrá un usuario.
        # Si la prueba se corre en vivo, podría requerirse crear el usuario previamente.
        self.token = None
        self.user_email = f"locust{random.randint(1, 10000)}@example.com"
        self.user_password = "test_password"
        
        # Opcional: Registrar usuario para que luego se pueda loguear
        # Por seguridad y no saturar, simulamos solo si hay endpoint de registro habilitado, 
        # sino, usaremos un usuario fijo. En este caso intentaremos usar un usuario fijo
        # que se asume debe estar en la BD.
        self.fixed_user = "test@example.com"

    @task(4)
    def view_public_data(self):
        """Flujo de Lectura: Simula a un visitante viendo el portal (80% del tráfico)."""
        self.client.get("/trabajos", name="Obtener Trabajos")
        self.client.get("/albergues", name="Obtener Albergues")
        self.client.get("/mascotas_perdidas", name="Obtener Mascotas Perdidas")

    @task(1)
    def transactional_flow(self):
        """Flujo Transaccional: Login y publicación (20% del tráfico)."""
        # Paso 1: Intentar hacer Login
        response = self.client.post("/login", json={
            "email": self.fixed_user,
            "contraseña": "secretpassword" # Reemplazar con credencial válida si se requiere Auth real
        }, name="Login")

        if response.status_code == 200:
            data = response.json()
            if "token" in data:
                self.token = data["token"]

        # Paso 2: Si el login fue exitoso y tenemos token, intentamos publicar un trabajo.
        if self.token:
            payload = {
                "nombre": "Trabajo de Carga",
                "ubicacion": "CDMX",
                "fechaPublicacion": "2024-01-01",
                "monto": float(random.randint(100, 500)),
                "descripcion": "Descripción generada por Locust",
                "idAnimalLoverPublicador": 1, # ID dummy
                "tipoTrabajo": "Servicio",
                "imagenesBase64": ["data:image/png;base64,img"]
            }
            
            self.client.post(
                "/trabajo", 
                json=payload, 
                headers={"Authorization": self.token},
                name="Publicar Trabajo (Auth)"
            )
