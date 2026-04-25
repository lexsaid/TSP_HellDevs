FROM python:3.11-slim

WORKDIR /app

# Instalar SQLite3 por si es util dentro del contenedor para debug
RUN apt-get update && apt-get install -y sqlite3 --no-install-recommends && rm -rf /var/lib/apt/lists/*

# Copiar archivos
COPY . .

# Instalar dependencias
# Como se solicito mantenerlo lo mas simple y con librerias estrictamente necesarias:
RUN pip install --no-cache-dir fastapi uvicorn pydantic

EXPOSE 40000

# Añadir el directorio base al PYTHONPATH para los imports
ENV PYTHONPATH=/app

# Comando para ejecutar el enrutador
CMD ["python", "-m", "enrutador.enrutador"]