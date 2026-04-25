import sqlite3
import os

# Function to get a connection to the database
def getDbConnection():
    dbPath = os.getenv("DB_PATH", "/app/app/mizcuin.db")
    # Para pruebas en local si no existe la ruta de docker, usamos el directorio local
    if not os.path.exists(os.path.dirname(dbPath)) and dbPath == "/app/app/mizcuin.db":
        dbPath = "mizcuin.db"

    conn = sqlite3.connect(dbPath)
    # Return rows as dictionary-like objects
    conn.row_factory = sqlite3.Row
    return conn
