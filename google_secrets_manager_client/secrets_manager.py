import os

from google.cloud import secretmanager

PROJECT_ID = "secret-manager-322613"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(
    os.getcwd(),
    "secret-manager-322613-56722a79fc96.json"
)


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
