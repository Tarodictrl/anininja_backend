import requests

from app.core.settings import settings


class VK:
    @staticmethod
    async def validate_auth_token(code: str, redirect_uri: str) -> dict | None:
        url = "https://oauth.vk.com/access_token"
        client_id = settings.client_id
        secret_key = settings.secret_key
        params = dict(client_id=client_id, client_secret=secret_key, code=code, redirect_uri=redirect_uri)
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        return

    async def get_user_info(token: str, id: int) -> dict | None:
        url = "https://api.vk.com/method/account.getProfileInfo"
        data = dict(access_token=token, v=5.199)
        response = requests.get(url, params=data)
        if response.status_code == 200:
            return response.json()["response"]
        return
