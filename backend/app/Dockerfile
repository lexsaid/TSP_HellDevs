# ETAPA 1: Constructor (Builder)
FROM golang:1.25-bookworm AS builder

# Instalamos dependencias de compilación para SQLite (CGO)
RUN apt-get update && apt-get install -y \
    gcc \
    libc6-dev \
    sqlite3 \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Gestionar dependencias
COPY go.mod go.sum ./
RUN go mod download

# Copiar el código y compilar
COPY . .
# CGO_ENABLED=1 es OBLIGATORIO para SQLite
RUN CGO_ENABLED=1 GOOS=linux go build -o main ./interface/

# ---------------------------------------------------------

# ETAPA 2: Ejecutor (Runtime)
FROM debian:bookworm-slim

# Instalamos la librería de tiempo de ejecución de SQLite
RUN apt-get update && apt-get install -y \
    libsqlite3-0 \
    ca-certificates \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copiamos solo el ejecutable desde la etapa anterior
COPY --from=builder /app/main .

# Exponemos el puerto de tu backend
EXPOSE 40000

# Ejecutamos el binario directamente (más rápido y seguro)
CMD ["./main"]