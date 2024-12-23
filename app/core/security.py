import base64
from datetime import datetime, timedelta, timezone

import requests
from fastapi import HTTPException, status
from Crypto.Cipher import AES
import jwt
from jwt.exceptions import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.settings import settings
from app.core.logger import logging
from app.core.controllers.user import user_crud

UNAUTHORIZED_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=30)
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode, settings.password_secret_key, algorithm="HS256")
    return encode_jwt


def encrypt_password(password: str) -> str:
    cipher = AES.new(settings.password_secret_key.encode(), AES.MODE_ECB)
    return base64.b64encode(cipher.encrypt(password.encode().rjust(32))).decode()


def decrypt_password(password: str) -> str:
    cipher = AES.new(settings.password_secret_key, AES.MODE_ECB)
    return cipher.decrypt(base64.b64decode(password.encode()))


def verify_turnstile_token(token: str) -> bool:
    try:
        response = requests.post(
            'https://challenges.cloudflare.com/turnstile/v0/siteverify',
            data={'secret': settings.cloudflare_turnstile_key, 'response': token}
        )
        result = response.json()
        return result.get('success', False)
    except requests.RequestException as e:
        logging.error(e, exc_info=True)
        return False


def verify_access_token(access_token: str) -> int:
    try:
        payload = jwt.decode(access_token, settings.password_secret_key, algorithms=["HS256"])
        id: str = payload.get("sub")
        if id is None:
            raise UNAUTHORIZED_EXCEPTION
        return int(id)
    except InvalidTokenError:
        raise UNAUTHORIZED_EXCEPTION


async def validate_permission(user_id: int, permission: str, session: AsyncSession):
    user = await user_crud.get_by_id(session=session, obj_id=user_id)
    if user is None:
        raise UNAUTHORIZED_EXCEPTION
    if user.role is None:
        raise UNAUTHORIZED_EXCEPTION
    if user.role != permission:
        raise UNAUTHORIZED_EXCEPTION
