
from typing_extensions import Annotated
import re

from fastapi import APIRouter, status, Depends, HTTPException, Response, Cookie
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.controllers.user import user_crud
from app.core.schemas.user import (
    LoginSchema,
    RegistrationSchema,
    UserBase,
    UserRegistration,
    UserPrivateResponseBase,
)
from app.core.security import (
    create_access_token,
    encrypt_password,
    verify_access_token,
    verify_turnstile_token
)
from app.api.endpoints.user.vk import VK
from app.core.settings import settings

router: APIRouter = APIRouter()

EMAIL_REGEX = "(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"


@router.post(
    "/registration",
    status_code=status.HTTP_201_CREATED,
)
async def user_registration(
    response: Response,
    data: RegistrationSchema,
    session: Annotated[AsyncSession, Depends(get_async_session)],
):
    data: dict = data.model_dump()
    data.update(password=encrypt_password(data["password"]))
    if not verify_turnstile_token(data.pop("token")):
        raise HTTPException(status_code=400, detail="Неверная капча.")
    if not re.findall(EMAIL_REGEX, data["email"]):
        raise HTTPException(status_code=400, detail="Неверная почта.")
    if await user_crud.get_by_attribute(attr_name="login", attr_value=data["login"], session=session):
        raise HTTPException(status_code=400, detail="Данный логин уже занят.")
    if await user_crud.get_by_attribute(attr_name="email", attr_value=data["email"], session=session):
        raise HTTPException(status_code=400, detail="Данная почта уже зарегистрирована.")
    obj_in = UserRegistration(**data)
    obj_db = await user_crud.create(obj_in=obj_in, session=session)
    access_token = create_access_token({"sub": str(obj_db.id)})
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    return {'access_token': access_token}


@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
)
async def user_login(
    response: Response,
    data: LoginSchema,
    session: Annotated[AsyncSession, Depends(get_async_session)],
):
    data: dict = data.model_dump()
    data.update(password=encrypt_password(data["password"]))
    if not verify_turnstile_token(data.pop("token")):
        raise HTTPException(status_code=400, detail="Неверная капча.")
    user = await user_crud.get_by_creditionals(login_or_email=data["login"], hashed_password=data["password"], session=session)
    if not user:
        raise HTTPException(status_code=401, detail="Неверные данные для входа.")
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie(
        key="access_token",
        value=access_token,
        expires=60 * 60 * 24 * 7
    )
    return {'access_token': access_token}


@router.get(
    "/vk_auth",
    status_code=status.HTTP_200_OK,
)
async def user_vk_auth(
    code: str,
    session: Annotated[AsyncSession, Depends(get_async_session)],
):
    response = await VK.validate_auth_token(code, settings.redirect_auth_uri)
    if response is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid code.")
    user_info = await VK.get_user_info(token=response.get("access_token"),
                                       id=response.get("user_id"))
    user = await user_crud.get_by_attribute(session=session, attr_name="vk_id", attr_value=user_info.get("id"))
    if user is None:
        user_model = UserBase.model_validate(dict(
            vk_id=user_info.get("id"),
            avatar=user_info.get("photo_200"),
            login=user_info.get("screen_name")), strict=True)
        user = await user_crud.create(session=session, obj_in=user_model)
    response = RedirectResponse(url=settings.host)
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie(
        key="access_token",
        value=access_token,
        expires=60 * 60 * 24 * 7
    )
    return response


@router.get(
    "/vk_connect",
    status_code=status.HTTP_200_OK,
)
async def user_vk_connect(
    code: str,
    session: Annotated[AsyncSession, Depends(get_async_session)],
    access_token: str | None = Cookie(default=None),
):
    response = await VK.validate_auth_token(code, redirect_uri=settings.redirect_connect_uri)
    if response is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid code.")
    vk_id = response.get("user_id")
    already_connected = await user_crud.get_by_attribute(session=session, attr_name="vk_id", attr_value=vk_id)
    if already_connected:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This vk account is already connected to another user.")
    user_id = verify_access_token(access_token)
    user = await user_crud.get_by_attribute(session=session, attr_name="id", attr_value=user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid access token.")

    update_dict = {"vk_id": vk_id}
    user = await user_crud.update(session=session, db_obj=user, obj_in=update_dict)

    response = RedirectResponse(url=settings.host + "/profile")
    return {"status": "ok"}


@router.get(
    "/profile",
    response_model=UserPrivateResponseBase,
    status_code=status.HTTP_200_OK,
)
async def get_profile(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    access_token: str | None = Cookie(default=None),
):
    user_id = verify_access_token(access_token)
    user = await user_crud.get_profile(id=user_id, session=session)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
