import os
from typing import List

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    # encryption vars
    encryption_key: str = Field(env='ENCRYPTION_KEY')

    # outlook client vars
    outlook_client_secret: str = Field(env='OUTLOOK_APP_SECRET')
    outlook_client_id: str = "e5998309-9706-4897-b8b5-efc1ea6cd347"
    outlook_authority: str = "https://login.microsoftonline.com/common"
    redirect_path: str = "/getAToken"
    redirect_uri: str = f"http://127.0.0.1:5000{redirect_path}"
    user_endpoint: str = "https://graph.microsoft.com/v1.0/me/"
    event_endpoint: str = f'{user_endpoint}events/'
    scope: List = ["Calendars.ReadWrite", "User.Read"]
    SESSION_TYPE = "filesystem"

    # secret manager vars
    google_project_id: str = Field(env="GOOGLE_PROJECT_ID")
    google_application_creds = os.path.join(
        os.getcwd(),
        "secret-manager-322613-56722a79fc96.json"
    )
    google_service_private_key: str = "str"
    # google_service_private_key: str = Field(env="GOOGLE_PRIVATE_KEY")

    # app config
    SECRET_KEY = "test"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    database_uri: str = Field(env="DATABASE_URI")
