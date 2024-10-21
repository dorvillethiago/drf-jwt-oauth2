from requests import post, get
from django.conf import settings


class GoogleAuthService:
    def __init__(self):
        self.client_id = settings.GOOGLE_CLIENT_ID
        self.client_secret = settings.GOOGLE_CLIENT_SECRET

    def get_user_token(self, code: str) -> str:
        token_url = "https://oauth2.googleapis.com/token"
        payload = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": "http://localhost:8000/auth/google/callback/",
        }

        token_response = post(token_url, data=payload)
        token_response_data = token_response.json()

        access_token = token_response_data.get("access_token")
        if not access_token:
            raise Exception("Failed to obtain access token.")

        return access_token

    def get_user_info(self, access_token: str) -> dict:
        user_info_url = "https://www.googleapis.com/oauth2/v2/userinfo"
        headers = {"Authorization": f"Bearer {access_token}"}
        user_info_response = get(user_info_url, headers=headers)

        if user_info_response.status_code != 200:
            raise Exception("Failed to fetch user information.")

        user_info = user_info_response.json()

        return user_info
