import os
import sqlite3
import sys
from pathlib import Path
from itertools import count

import pytest
from fastapi.testclient import TestClient

ROOT_DIR = Path(__file__).resolve().parents[1]
BACKEND_DIR = ROOT_DIR / "backend"
APP_DIR = BACKEND_DIR / "app"

if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))


@pytest.fixture()
def db_path(tmp_path, monkeypatch):
    """Crea una base de datos SQLite en memoria para cada sesión de test."""
    db_file = tmp_path / "test_bdd.db"
    monkeypatch.setenv("DB_PATH", str(db_file))

    schema_path = BACKEND_DIR / "docs" / "sentencia.sql"
    schema_sql = schema_path.read_text(encoding="utf-8")

    conn = sqlite3.connect(db_file)
    conn.executescript(schema_sql)
    conn.commit()
    conn.close()

    return db_file


@pytest.fixture()
def client(db_path, monkeypatch):
    """Instancia de TestClient con la DB configurada y reseteo de dependencias."""
    from enrutador import enrutador as api

    async def no_op_reset():
        return None

    monkeypatch.setattr(api, "resetTokensJob", no_op_reset)

    with TestClient(api.app) as test_client:
        yield test_client


@pytest.fixture()
def seed_user(db_path):
    """Permite crear un usuario rápidamente en la BD de pruebas."""
    from manejadores import manejadorUsuario
    from modelos.modelos import AnimalLover
    from repositorios import usuarioRepo

    counter = count(1)

    def _seed_user(nombre="Bdd", apellido="User", email=None, telefono=None, contrasena="bdd123"):
        idx = next(counter)
        if not email:
            email = f"bdd{idx}@example.com"
        if not telefono:
            telefono = f"555{idx:07d}"

        user = AnimalLover(
            nombre=nombre,
            apellido=apellido,
            email=email,
            telefono=telefono,
            **{"contraseña": contrasena},
        )
        ok = manejadorUsuario.guardarUsuario(user)
        if not ok:
            raise RuntimeError(f"No se pudo insertar usuario: {email}, {telefono}")
        saved, _ = usuarioRepo.buscarPorEmail(email)
        return saved

    return _seed_user


@pytest.fixture()
def seed_trabajo(db_path, seed_user):
    """Permite crear un trabajo rápidamente en la BD de pruebas."""
    from repositorios import trabajoRepo
    from modelos.modelos import Trabajo

    counter = count(1)

    def _seed_trabajo(nombre="Paseo", id_publicador=None, tipo="Servicio"):
        if id_publicador is None:
            idx = next(counter)
            user = seed_user(
                email=f"publicador{idx}@example.com",
                telefono=f"11{idx:08d}",
            )
            id_publicador = user.idAnimalLover

        trabajo = Trabajo(
            nombre=nombre,
            ubicacion="CDMX",
            fechaPublicacion="2024-01-01",
            monto=100.0,
            descripcion="Descripcion",
            idAnimalLoverPublicador=id_publicador,
            tipoTrabajo=tipo,
        )
        consulta = "INSERT INTO trabajo (nombre, ubicacion, fecha_publicacion, monto, descripcion, id_animalLover_publicador, tipo_trabajo) VALUES (?, ?, ?, ?, ?, ?, ?)"
        trabajo_id = trabajoRepo.guardarTrabajo(consulta, trabajo)
        return trabajo_id

    return _seed_trabajo
