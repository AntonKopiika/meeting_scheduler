import json
import os

from google.cloud import secretmanager

from meeting_scheduler.app_config import Settings

settings = Settings()
PROJECT_ID = settings.google_project_id


def init_secret_manager():
    with open(settings.google_application_creds, 'r+') as file:
        file_data = json.load(file)
        print(file_data)
        file_data["private_key"] = settings.google_service_private_key
        file.seek(0)
        json.dump(file_data, file, indent=4)
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = settings.google_application_creds


def create_secret(secret_id):
    client = secretmanager.SecretManagerServiceClient()
    parent = f"projects/{PROJECT_ID}"
    secret = {'replication': {'automatic': {}}}
    secrets = client.list_secrets(parent=parent)
    secrets_list = [
        page.secrets[i].name
        for page in secrets.pages
        for i in range(secrets.total_size)
    ]
    if f"projects/433787392673/secrets/{secret_id}" not in secrets_list:
        client.create_secret(secret_id=secret_id, parent=parent, secret=secret)


def add_secret_version(secret_id, payload):
    client = secretmanager.SecretManagerServiceClient()
    parent = f"projects/{PROJECT_ID}/secrets/{secret_id}"
    payload = payload.encode('UTF-8')
    client.add_secret_version(parent=parent, payload={'data': payload})


def access_secret_version(secret_id, version_id="latest"):
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{PROJECT_ID}/secrets/{secret_id}/versions/{version_id}"
    response = client.access_secret_version(name=name)
    return response.payload.data.decode('UTF-8')


def remove_secret(secret_id):
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{PROJECT_ID}/secrets/{secret_id}"
    client.delete_secret(name=name)
