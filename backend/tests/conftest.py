import os
import sqlite3
import sys
from pathlib import Path
from itertools import count

import pytest
from fastapi.testclient import TestClient


ROOT_DIR = Path(__file__).resolve().parents[1]
APP_DIR = ROOT_DIR / "app"
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))


@pytest.fixture()
def db_path(tmp_path, monkeypatch):
    db_file = tmp_path / "test.db"
    monkeypatch.setenv("DB_PATH", str(db_file))

    schema_path = ROOT_DIR / "docs" / "sentencia.sql"
    schema_sql = schema_path.read_text(encoding="utf-8")

    conn = sqlite3.connect(db_file)
    conn.executescript(schema_sql)
    conn.commit()
    conn.close()

    return db_file


@pytest.fixture()
def client(db_path, monkeypatch):
    from enrutador import enrutador as api
    from enrutador.AuthMiddleware import validarSesion

    async def no_op_reset():
        return None

    monkeypatch.setattr(api, "resetTokensJob", no_op_reset)
    api.app.dependency_overrides[validarSesion] = lambda: 1

    with TestClient(api.app) as test_client:
        yield test_client

    api.app.dependency_overrides.clear()


@pytest.fixture()
def fetch_scalar(db_path):
    def _fetch_scalar(query, params=()):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        row = cursor.fetchone()
        conn.close()
        return row[0] if row else None

    return _fetch_scalar


@pytest.fixture()
def seed_user(db_path):
    from manejadores import manejadorUsuario
    from modelos.modelos import AnimalLover
    from repositorios import usuarioRepo

    def _seed_user(nombre="Test", apellido="User", email="test@example.com", telefono="1234567890", contrasena="secret"):
        user = AnimalLover(
            nombre=nombre,
            apellido=apellido,
            email=email,
            telefono=telefono,
            **{"contraseña": contrasena},
        )
        ok = manejadorUsuario.guardarUsuario(user)
        if not ok:
            raise RuntimeError("No se pudo insertar usuario")
        saved, _ = usuarioRepo.buscarPorEmail(email)
        return saved

    return _seed_user


@pytest.fixture()
def seed_trabajo(db_path, seed_user):
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


@pytest.fixture()
def seed_albergue(db_path, seed_user):
    from repositorios import alberguesRepo
    from modelos.modelos import Albergue

    def _seed_albergue(nombre="Albergue Uno", id_dueno=None):
        if id_dueno is None:
            user = seed_user(email="albergue@example.com", telefono="2222222222")
            id_dueno = user.idAnimalLover

        albergue = Albergue(
            idAnimalLover=id_dueno,
            nombre=nombre,
            ubicacion="CDMX",
            capacidad=10,
            preferencia="Perros",
            costoDiario=50,
            preRequisitos="Requisitos",
        )
        albergue_id = alberguesRepo.guardarAlbergue(albergue)
        return albergue_id

    return _seed_albergue
