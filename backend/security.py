"""OIDC JWT validado no servidor. NUNCA há modo de login de demonstração público."""
from __future__ import annotations
from functools import lru_cache
from typing import Annotated
import os
import jwt
from jwt import PyJWKClient
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, Field, ValidationError


class Principal(BaseModel):
    sub: str = Field(min_length=1)
    roles: list[str] = Field(default_factory=list)
    unit_codes: list[str] = Field(default_factory=list)
    permissions: list[str] = Field(default_factory=list)


bearer = HTTPBearer(auto_error=False)


@lru_cache(maxsize=1)
def jwks_client() -> PyJWKClient:
    return PyJWKClient(os.environ["OIDC_JWKS_URL"], cache_keys=True, lifespan=300)


def get_principal(credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer)]) -> Principal:
    if not all(os.environ.get(key) for key in ("OIDC_JWKS_URL", "OIDC_ISSUER", "OIDC_AUDIENCE")):
        raise HTTPException(503, "Provedor de identidade institucional não configurado.")
    if not credentials or credentials.scheme.lower() != "bearer":
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Token Bearer exigido.", headers={"WWW-Authenticate": "Bearer"})
    try:
        token = credentials.credentials
        signing_key = jwks_client().get_signing_key_from_jwt(token).key
        payload = jwt.decode(token, signing_key, algorithms=["RS256"], audience=os.environ["OIDC_AUDIENCE"], issuer=os.environ["OIDC_ISSUER"], options={"require": ["exp", "iat", "sub", "iss", "aud"]}, leeway=30)
        return Principal(sub=str(payload["sub"]), roles=payload.get("roles", []), unit_codes=payload.get("unit_codes", []), permissions=payload.get("permissions", []))
    except (jwt.PyJWTError, ValidationError, ValueError, KeyError, TypeError) as error:
        raise HTTPException(401, "Token inválido ou expirado.", headers={"WWW-Authenticate": "Bearer"}) from error


def require(permission: str, user: Principal) -> None:
    if permission not in user.permissions:
        raise HTTPException(403, f"Permissão {permission} não concedida.")


def authorize_record(user: Principal, record, operation: str = "read") -> None:
    permission = f"records:{operation}"
    if permission not in user.permissions:
        raise HTTPException(403, "Permissão insuficiente.")
    if record.unit_code not in user.unit_codes and f"records:{operation}:all" not in user.permissions:
        raise HTTPException(404, "Registro não encontrado.")
    if record.classification == "restrito" and f"records:restricted:{operation}" not in user.permissions:
        raise HTTPException(404, "Registro não encontrado.")
