import string

import pytest
from fastapi import HTTPException
from starlette.requests import Request

from enrutador import AuthMiddleware
from repositorios import usuarioRepo


def test_generar_token_formato_hex():
    # Arrange
    # Act
    token = AuthMiddleware.generarToken()

    # Assert
    assert len(token) == 64
    assert all(ch in string.hexdigits for ch in token)


def test_crear_sesion_actualiza_token(seed_user):
    # Arrange
    user = seed_user(email="token@example.com", telefono="3333333333")

    # Act
    token = AuthMiddleware.crearSesion(user.idAnimalLover)

    # Assert
    usuario, ok = usuarioRepo.buscarPorToken(token)
    assert ok is True
    assert usuario.idAnimalLover == user.idAnimalLover


def test_crear_sesion_falla_si_no_actualiza(monkeypatch):
    # Arrange
    monkeypatch.setattr(usuarioRepo, "actualizarToken", lambda _id, _t: False)

    # Act / Assert
    with pytest.raises(HTTPException) as exc:
        AuthMiddleware.crearSesion(1)
    assert exc.value.status_code == 500


def test_validar_sesion_sin_token_lanza_error():
    # Arrange
    request = Request({"type": "http", "method": "GET", "path": "/", "headers": []})

    # Act / Assert
    with pytest.raises(HTTPException) as exc:
        AuthMiddleware.validarSesion(request, authorization=None)
    assert exc.value.status_code == 401


def test_validar_sesion_token_invalido_lanza_error(monkeypatch):
    # Arrange
    request = Request({"type": "http", "method": "GET", "path": "/", "headers": []})
    monkeypatch.setattr(usuarioRepo, "buscarPorToken", lambda _t: (None, False))

    # Act / Assert
    with pytest.raises(HTTPException) as exc:
        AuthMiddleware.validarSesion(request, authorization="bad-token")
    assert exc.value.status_code == 401


def test_validar_sesion_valida_asigna_state(seed_user):
    # Arrange
    user = seed_user(email="auth@example.com", telefono="4444444444")
    token = AuthMiddleware.crearSesion(user.idAnimalLover)
    request = Request({"type": "http", "method": "GET", "path": "/", "headers": []})

    # Act
    result = AuthMiddleware.validarSesion(request, authorization=token)

    # Assert
    assert result == user.idAnimalLover
    assert request.state.idUsuario == user.idAnimalLover
