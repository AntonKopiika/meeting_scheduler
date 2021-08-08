import os

CLIENT_ID = "11cbfe8a-6c4f-4fde-86c3-0c39fce7413d"

CLIENT_SECRET = os.getenv("OUTLOOK_APP_SECRET")

AUTHORITY = "https://login.microsoftonline.com/common"

REDIRECT_PATH = "/getAToken"
REDIRECT_URI = f"https://www.mymeeeting.com{REDIRECT_PATH}"

USER_ENDPOINT = "https://graph.microsoft.com/v1.0/me/"
EVENT_ENDPOINT = f'{USER_ENDPOINT}events/'

SCOPE = ["Calendars.ReadWrite", "User.Read"]
SESSION_TYPE = "filesystem"
