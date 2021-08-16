import os

CLIENT_ID = "e5998309-9706-4897-b8b5-efc1ea6cd347"

# CLIENT_SECRET = os.getenv("OUTLOOK_APP_SECRET")
CLIENT_SECRET = "U~HTd1xXBRb7U.e3ndj-.8Sib.xSt8yr0Y"
AUTHORITY = "https://login.microsoftonline.com/common"

REDIRECT_PATH = "/getAToken"
REDIRECT_URI = f"https://www.mymeeeting.com{REDIRECT_PATH}"

USER_ENDPOINT = "https://graph.microsoft.com/v1.0/me/"
EVENT_ENDPOINT = f'{USER_ENDPOINT}events/'

SCOPE = ["Calendars.ReadWrite", "User.Read"]
SESSION_TYPE = "filesystem"
