import os

CLIENT_ID = "11cbfe8a-6c4f-4fde-86c3-0c39fce7413d"

CLIENT_SECRET = "dQb2BbHyW3..632L7tDb.9j8a1-gi57e6L"

# CLIENT_SECRET = os.environ.get("OUTLOOK_APP_SECRET")
if not CLIENT_SECRET:
    raise ValueError("Need to define CLIENT_SECRET environment variable")

AUTHORITY = "https://login.microsoftonline.com/common"

REDIRECT_PATH = "/getAToken"

ENDPOINT = 'https://graph.microsoft.com/v1.0/me/events/'

SCOPE = ["Calendars.ReadWrite"]
SESSION_TYPE = "filesystem"
